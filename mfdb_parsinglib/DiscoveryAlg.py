import queue
from collections import defaultdict
import math

from .DiscoveryOptions import DiscoveryOptions
from .attributes import EDBSource, EDB_SOURCES, EDB_SOURCES_OTHER, is_supported
from .edb_formatting import parsinglib, depad_id, pad_id
from .managers.EDBManager import EDBManager
from .managers.OptionsManager import OptionsManager
from .views.MetaboliteDiscovery import MetaboliteDiscovery

EDB_REF = tuple[str, str]
QUEUE_ITEM = tuple[EDB_REF, EDB_REF]


class DiscoveryAlg:
    """
    EDB Manager that utilizes a local relational database to access EDB sources.
    It still uses remote API
    """

    """
    Queue that drives the discovery algorithm.
    - First tuple is the EDB reference (EDB source + EDB ID) to be resolved
    - Second tuple is the EDB reference that referenced the first EDB ID
    """
    Q: queue.Queue[QUEUE_ITEM]
    """
    Queue items that have failed to be resolved
    """
    undiscovered: set[QUEUE_ITEM]
    """
    Lists EDB_IDs and ref-attributes that have been successfully queries or fetched by the algorithm
    """
    discovered: set[EDB_REF]
    """
    EDB references that have already been in the queue (as the first item in QUEUE_ITEM)
    This guarantees that the BFS algorithm eventually stops
    """
    been_in_queue: set[EDB_REF]

    def __init__(self):
        # Discovery options defined for each EDB source
        self.verbose = False
        self.reverse_lookup: set[str] = set()
        self.discoverable_attributes: set[str] = set()

        # Data sets and state variables used for the algorithm
        self.Q = queue.Queue()
        self.undiscovered = set()
        self.secondary_ids = set()
        self.ambiguous = []
        self.discovered = set()
        self.been_in_queue = set()
        self.reverse_lookup_ran = False

        # main object to aggregate EDB sources
        self.meta: MetaboliteDiscovery | None = None

        # EDB manager
        self.opts = OptionsManager()
        self.mgr = EDBManager(self.secondary_ids, self.opts)

    def run_discovery(self):
        """
        Using a queue,
        :return:
        """

        while not self.Q.empty():
            edb_ref, edb_src = self.Q.get()

            # Query metabolite record from local database or web api
            if self.verbose:
                print(f"  {edb_src[0]}[{edb_src[1]}] -> {edb_ref[0]}[{edb_ref[1]}]")

            # todo: @ITT: BUG edb_id is the SOURCE id not the explorable one!!!!!
            edb_record = self.mgr.get_metabolite(*edb_ref)

            if not edb_record:
                self.undiscovered.add((edb_ref, edb_src))
                continue

            # edb record was discovered, add it to previously discovered data:
            # if edb_record.mass is not None and math.isnan(edb_record.mass) or edb_record.mi_mass is not None and math.isnan(edb_record.mi_mass):
            #     print("NAN MASS: ", edb_record.edb_id, edb_record.edb_source, edb_record.mass, edb_record.mi_mass)
            self.meta.merge(edb_record)
            self.discovered.add(edb_ref)

            self.find_novel_ids(edb_ref, edb_record)

            if self.Q.empty() and not self.reverse_lookup_ran:
                # once we ran out of ids to explore, try reverse queries as a final attempt
                self.resolve_reverse_queries()

        return self.finish_discovery()

    def find_novel_ids(self, edb_ref, edb_record):
        found_new = False

        # find novel EDB IDs and attribute references within this view
        opts = self.opts.get_opts(edb_ref[0])
        for attr in self.discoverable_attributes:
            val = depad_id(getattr(edb_record, attr), attr)

            if val:
                edb_new = (attr, val)
                self.enqueue(edb_new, edb_ref)
                found_new = True
        return found_new

    def enqueue(self, edb_ref: EDB_REF, edb_src: EDB_REF):

        # todo: @later: support attribute queries too?
        if not is_supported(edb_ref):
            # unsupported EDB source, no need to enqueue because it can't be resolved by the manager
            self.undiscovered.add((edb_ref, edb_src))
            return False
        elif edb_ref not in self.been_in_queue and edb_ref != edb_src:
            # enqueue for exploration, but only if it hasn't occurred before
            self.Q.put((edb_ref, edb_src))
            self.been_in_queue.add(edb_ref)
        return True

    def resolve_reverse_queries(self):
        """
        This is used for a final attempt to reverse query existing EDB Ids and attributes
        by querying in reverse (querying on the foreign keys of EDB table rather than its pkey EDB_ID)
        we discover additional items that are added to the queue for natural resolve
        :return:
        """
        # missing ref value is empty list or sometimes None
        #reverse_attrs = list(filter(lambda at: not getattr(self.meta, at), self.reverse_lookup))
        if not self.reverse_lookup:
            return

        if self.verbose:
            print('Reverse-querying', ', '.join(self.reverse_lookup))
        self.reverse_lookup_ran = True

        edb_records = self.mgr.get_reverse(self.meta, *self.reverse_lookup)

        for edb_record in edb_records:
            if edb_record.mass is not None and math.isnan(edb_record.mass) or edb_record.mi_mass is not None and math.isnan(edb_record.mi_mass):
                print("NAN MASS(rev): ", edb_record.edb_id, edb_record.edb_source, edb_record.mass, edb_record.mi_mass)
            self.meta.merge(edb_record)

            edb_ref = (edb_record.edb_source, edb_record.edb_id)

            found_new = self.find_novel_ids(edb_ref, edb_record)

            if found_new:
                # reset flag if we found at least one new ID
                self.reverse_lookup_ran = False

                if self.verbose:
                    print("   revseq- ", *edb_ref)

        return edb_records

    def finish_discovery(self):
        assert self.Q.empty()

        # remove secondary IDs from discovery result
        for edb_tag, edb_id in self.secondary_ids:
            s: set = getattr(self.meta, edb_tag)
            s.discard(depad_id(edb_id, edb_tag))
            s.discard(pad_id(edb_id, edb_tag))

        # todo: @later: clear and return an object representing all the data
        #self.clear()

        if self.verbose:
            print("\nDiscovery finished!\n---------------------------------\n")

    def add_input(self, meta: MetaboliteDiscovery, edb_source: EDBSource = None):
        """
        Adds fields of input MetaboliteDiscovery view to the resolve queue
        :param meta: metabolite discovery object
        :param edb_source: EDB source tag (e.g. pubchem)
        :return:
        """
        # attributes to resolve
        opts = self.opts.get_opts(edb_source)
        self.meta = meta

        for edb_tag in self.discoverable_attributes:
            edb_id = parsinglib.try_flatten(getattr(meta, edb_tag))

            if edb_id:
                if self.verbose:
                    print("  Adding input:", edb_id, edb_tag)
                edb_id = depad_id(edb_id, edb_tag)
                self.enqueue((edb_tag, edb_id), ("root_input", "-"))

    def add_scalar_input(self, edb_source: EDBSource, edb_id):
        meta = MetaboliteDiscovery()
        getattr(meta, edb_source.value+'_id').add(edb_id)
        self.add_input(meta, edb_source)
        return self.meta

    def clear(self):
        self.Q = queue.Queue()

        self.undiscovered.clear()
        self.secondary_ids.clear()
        self.ambiguous.clear()
        self.discovered.clear()
        self.been_in_queue.clear()
        self.reverse_lookup_ran = False
