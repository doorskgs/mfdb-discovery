from .attributes import COMMON_ATTRIBUTES, EDB_ID_OTHER, EDB_SOURCES


class DiscoveryOptions:

    def __init__(self):
        self.edb_source: str | None = None
        self.cache_enabled = True
        self.cache_predump = True

        """
        Attributes used to resolve
        """
        self.attr: set = set()

        """
        EDB IDs used to resolve
        """
        self.edb_ids: set = set(map(lambda x: x+'_id', EDB_SOURCES))

    def __hash__(self):
        return hash(self.edb_source)
