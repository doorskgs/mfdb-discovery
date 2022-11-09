import requests

from .ApiClientBase import ApiClientBase
from .api_parsers.keggparser import parse_kegg
from ..attributes import EDB_SOURCES, EDB_SOURCES_OTHER
from ..edb_formatting import pad_id, remap_keys, preprocess, map_to_edb_format
from ..views.MetaboliteConsistent import MetaboliteConsistent


class KeggClient(ApiClientBase):
    _mapping = dict(
        name='names',
        exact_mass='mi_mass',
        mol_weight="mass",
    ) | {edb_tag: edb_tag+'_id' for edb_tag in (EDB_SOURCES|EDB_SOURCES_OTHER)}

    _important_attr = set()

    _reverse = (
        'chebi_id',
        'lipidmaps_id',
        # 'pubchem_id'
    )

    def fetch_api(self, edb_id):
        r = requests.get(url=f'http://rest.kegg.jp/get/cpd:{pad_id(edb_id, "kegg_id")}')

        data = parse_kegg(edb_id, r.text)

        remap_keys(data, self._mapping)
        preprocess(data)
        data, etc = map_to_edb_format(data, important_attr=self._important_attr)

        data['edb_source'] = 'kegg'
        return MetaboliteConsistent(**data)
