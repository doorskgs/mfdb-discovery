from metabolite_index import EDBSource
from metabolite_index.DiscoveryOptions import DiscoveryOptions


class OptionsManager:
    def __init__(self):
        self.opts: dict[str, DiscoveryOptions] = {}

    def get_opts(self, edb_source: str | EDBSource):
        if isinstance(edb_source, EDBSource):
            edb_source = edb_source.value

        if edb_source.endswith('_id'):
            edb_source = edb_source[:-3]

        return self.opts.get(edb_source, DiscoveryOptions())
