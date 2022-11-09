import queue
from collections import defaultdict

from .DiscoveryOptions import DiscoveryOptions
from .attributes import EDBSource, EDB_SOURCES, is_supported, COMMON_ATTRIBUTES
from .edb_formatting import parsinglib, depad_id
from .managers.EDBManager import EDBManager
from .views.MetaboliteDiscovery import MetaboliteDiscovery

EDB_REF = tuple[str, str]
QUEUE_ITEM = tuple[EDB_REF, EDB_REF]

EDB_ID_ATTR = set(map(lambda x: x+'_id', EDB_SOURCES))


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
        self.opts: dict[EDBSource, DiscoveryOptions] = defaultdict(DiscoveryOptions)
        self.verbose = False
        # What attributes to use for reversed lookup
        self.reverse_lookup: set[str] = COMMON_ATTRIBUTES | EDB_ID_ATTR

        # Data sets used for
        self.Q = queue.Queue()
        self.undiscovered = set()
        self.secondary_ids = set()
        self.ambiguous = []
        self.discovered = set()
        self.been_in_queue = set()

        # main object to aggregate EDB sources
        self.meta: MetaboliteDiscovery | None = None

        self.mgr = EDBManager(self.secondary_ids)

    def add_input(self, meta: MetaboliteDiscovery, edb_source: EDBSource = None):
        """
        Adds fields of input MetaboliteDiscovery view to the resolve queue
        :param meta: metabolite discovery object
        :param edb_source: EDB source tag (e.g. pubchem)
        :return:
        """
        # attributes to resolve
        opts = self.get_opts(edb_source)
        self.meta = meta

        for edb_tag in opts.edb_ids:
            edb_id = parsinglib.try_flatten(getattr(meta, edb_tag))

            if edb_id:
                edb_id = depad_id(edb_id, edb_tag)
                self.enqueue((edb_tag, edb_id), ("root_input", "-"))

    def run_discovery(self):
        """
        Using a queue,
        :return:
        """

        while not self.Q.empty():
            edb_ref, edb_src = self.Q.get()

            # Query metabolite record from local database or web api
            if self.verbose:
                print(f"{edb_src[0]}[{edb_src[1]}] -> {edb_ref[0]}[{edb_ref[1]}]")

            # todo: @ITT: BUG edb_id is the SOURCE id not the explorable one!!!!!
            edb_record = self.mgr.get_metabolite(*edb_ref)

            if not edb_record:
                self.undiscovered.add((edb_ref, edb_src))
                continue

            # edb record was discovered, add it to previously discovered data:
            self.meta.merge(edb_record)
            self.discovered.add(edb_ref)

            # find novel EDB IDs and attribute references within this view
            opts = self.get_opts(edb_ref[0])
            for attr in opts.edb_ids | opts.attr:
                val = depad_id(getattr(edb_record, attr), attr)

                if val:
                    edb_new = (attr, val)
                    self.enqueue(edb_new, edb_ref)

            if self.Q.empty():
            #     # once we ran out of ids to explore, try reverse queries as a final attempt
            #     self.resolve_reverse_queries()
                print("@TODO: REVERSE QUERY")

        if self.verbose:
            print("\nDiscovery finished!\n---------------------------------\n")
        assert self.Q.empty()

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
        reverse_attrs = filter(lambda at: not getattr(self.meta, at), self.reverse_lookup)

        if reverse_attrs:

            if self.verbose:
                print('Reverse-querying', reverse_attrs)

            edb_records = self.mgr.get_reverse(self.meta, *reverse_attrs)

            if edb_records:
                print(1, len(edb_records))
            # for attr, val in zip(reverse_attrs, attr_values):
            #     attr_ref = (attr, depad_id(val, attr))
            #     self.enqueue(attr_ref, ('reverseq', '[]'))

    def get_opts(self, edb_source: str | EDBSource):
        if isinstance(edb_source, str):
            if edb_source.endswith('_id'):
                edb_source = edb_source[:-3]

            edb_source = EDBSource(edb_source)

        return self.opts[edb_source] if edb_source else DiscoveryOptions()

    def clear(self):
        self.undiscovered.clear()
        self.secondary_ids.clear()
        self.ambiguous.clear()
        self.Q = queue.Queue()
        self.discovered.clear()
