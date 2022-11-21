import requests

from .ApiClientBase import ApiClientBase
from .api_parsers.keggparser import parse_kegg
from ..attributes import EDB_SOURCES, EDB_SOURCES_OTHER
from ..dal import ExternalDBEntity
from ..edb_formatting import pad_id, remap_keys, preprocess, map_to_edb_format


class KeggClient(ApiClientBase):
    url_base = 'http://rest.kegg.jp/get/'
    _reverse = (
        'chebi_id',
        'lipmaps_id',
        # 'pubchem_id'
    )

    def __init__(self):
        super().__init__()

        self.load_mapping('kegg')
        self._mapping.update((edb_tag, edb_tag+'_id') for edb_tag in (EDB_SOURCES|EDB_SOURCES_OTHER))


    def fetch_api(self, edb_id):
        r = requests.get(url=f'{self.url_base}cpd:{pad_id(edb_id, "kegg_id")}')

        content = r.text
        if r.status_code != 200 or not content:
            return None

        data = next(parse_kegg(r.iter_lines()))

        remap_keys(data, self._mapping)
        preprocess(data)
        data, etc = map_to_edb_format(data, important_attr=self._important_attr)

        return ExternalDBEntity(edb_source='kegg', **data)

    def fetch_api_bulk(self, edb_ids: list[str]):
        assert len(edb_ids) <= 10, "KEGG allows bulk queries in tens"
        # we don't pad/depad KEGG ids ('C' prefix), but we do have to add the 'cpd:' prefix
        _url = '+'.join(map(lambda x: 'cpd:'+x, edb_ids))
        r = requests.get(url=self.url_base+_url)

        content = r.text
        if r.status_code != 200 or not content:
            return None

        for data in parse_kegg(r.iter_lines()):

            remap_keys(data, self._mapping)
            preprocess(data)
            data, etc = map_to_edb_format(data, important_attr=self._important_attr)

            # todo: @later: for some reason, kegg's pubchem reference seems to be broken so we skip it
            data.pop('pubchem_id', None)

            yield ExternalDBEntity(edb_source='kegg', **data)
