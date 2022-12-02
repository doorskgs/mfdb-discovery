import queue
from collections import defaultdict
import math
from typing import Generator

from eme.mapper import map_to

from .DiscoveryOptions import DiscoveryOptions
from .attributes import EDBSource, EDB_SOURCES, EDB_SOURCES_OTHER, is_edb
from .edb_formatting import parsinglib, depad_id, pad_id
from .managers.EDBManager import EDBManager
from .managers.OptionsManager import OptionsManager
from .views.MetaboliteConsistent import MetaboliteConsistent
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

    async def run_discovery(self):
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
            edb_records = await self.mgr.get_metabolite(*edb_ref)

            if not edb_records:
                self.undiscovered.add((edb_ref, edb_src))
                continue

            self.discovered.add(edb_ref)

            for edb_record in edb_records:
                # edb record was discovered, add it to previously discovered data:
                self.meta.merge(edb_record)

                self.find_novel_ids(edb_ref, edb_record)

        return self.finish_discovery()

    def find_novel_ids(self, edb_ref: EDB_REF, edb_record: MetaboliteConsistent | MetaboliteDiscovery):
        """
        Parses edb_record's attributes and IDs that haven't been explored before and enqueues them for discovery

        :param edb_ref: EDB reference from which the record was found
        :param edb_record: external database record

        :return: true if new IDs/attributes were enqueued in record
        """
        found_new = False

        # find novel EDB IDs and attribute references within this view
        for edb_new in self.iter_discoverable(edb_record):
            self.enqueue(edb_new, edb_ref)
            found_new = True
        return found_new

    def enqueue(self, edb_ref: EDB_REF, edb_src: EDB_REF):

        if not edb_ref not in self.discoverable_attributes:
            # unsupported EDB source, no need to enqueue because it can't be resolved by the manager
            self.undiscovered.add((edb_ref, edb_src))
            return False
        elif edb_ref not in self.been_in_queue and edb_ref != edb_src:
            # enqueue for exploration, but only if it hasn't occurred before
            self.Q.put((edb_ref, edb_src))
            self.been_in_queue.add(edb_ref)
        return True

    def add_input(self, meta: MetaboliteDiscovery | MetaboliteConsistent, edb_source: EDBSource = None):
        """
        Adds fields of input MetaboliteDiscovery view to the resolve queue
        :param meta: metabolite discovery object
        :param edb_source: EDB source tag (e.g. pubchem)
        :return:
        """

        originating_edb_ref: EDB_REF = ("root_input", "-")
        self.find_novel_ids(originating_edb_ref, meta)

        consistent: MetaboliteConsistent
        if isinstance(meta, MetaboliteDiscovery):
            # map to consistent model
            self.meta = meta
        elif isinstance(meta, MetaboliteConsistent):
            self.meta = map_to(meta, MetaboliteDiscovery)
        else:
            raise ValueError()

        return self.meta

    def add_scalar_input(self, attribute: str | EDBSource, edb_id):
        if isinstance(attribute, EDBSource):
            attribute = attribute.value

        if is_edb(attribute):
            attribute = attribute+'_id'
        elif attribute not in self.discoverable_attributes:
            raise Exception(f"Attribute {attribute} is not configured to be discoverable. Please check your discovery config or the manual.")

        meta = MetaboliteDiscovery()

        getattr(meta, attribute).add(edb_id)

        return self.add_input(meta)

    def iter_discoverable(self, obj: MetaboliteDiscovery | MetaboliteConsistent) -> Generator[EDB_REF, None, None]:
        """

        :param obj:
        :return:
        """
        is_meta = isinstance(obj, MetaboliteDiscovery)

        for attr in self.discoverable_attributes:
            val = getattr(obj, attr)

            if val and is_meta:
                for child in val:
                    yield attr, depad_id(child, attr)
            elif val and not is_meta:
                yield attr, depad_id(val, attr)

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

    def clear(self):
        self.Q = queue.Queue()

        self.undiscovered.clear()
        self.secondary_ids.clear()
        self.ambiguous.clear()
        self.discovered.clear()
        self.been_in_queue.clear()
        self.reverse_lookup_ran = False
