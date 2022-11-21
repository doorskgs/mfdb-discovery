from collections import defaultdict

import requests

from .ApiClientBase import ApiClientBase
from ..edb_formatting import preprocess, map_to_edb_format, remap_keys, MultiDict, get_id_from_url
from ..dal import ExternalDBEntity


class PubchemClient(ApiClientBase):
    _reverse = (
        'chebi_id', 'hmdb_id', 'kegg_id'
    )

    _important_attr = {
        'logp'
    }

    def __init__(self):
        super().__init__()

        self.load_mapping('pubchem')

    def fetch_api(self, edb_id):
        r = requests.get(url=f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{edb_id}/json')
        r2 = requests.get(url=f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{edb_id}/xrefs/SBURL/json')

        # todo: description, synonyms, services

        s1 = r.status_code
        s2 = r2.status_code

        if (s1 != 200 and s1 != 304) or (s2 != 200 and s2 != 304):
            return None

        # todo: remake this as it's shady
        data = parse_pubchem(edb_id, r.json(), r2.json(), self._mapping)

        remap_keys(data, self._mapping)
        preprocess(data)
        data, etc = map_to_edb_format(data, important_attr=self._important_attr)

        data['edb_source'] = 'pubchem'
        return ExternalDBEntity(**data)


def parse_pubchem(edb_id, content, cont_refs, _mapping):
    """
    Parses API response for PubChem

    :param edb_id:
    :param c0:
    :param c1:
    :return:
    """

    data = MultiDict()

    # parse xrefs:
    _links = cont_refs['InformationList']['Information'][0]['SBURL']

    # guess xref IDs
    for link in _links:
        link = link.lower()

        db_id, api_db_tag = get_id_from_url(link)

        if db_id is None:
            # unrecognized XREF
            continue
        data.append(api_db_tag+'_id', db_id)


    _resp = content['PC_Compounds'][0]
    props = _resp.pop('props')
    data.append('pubchem_id',  _resp['id']['id']['cid'])

    hat_geci = []

    for prop in props:
        label = prop['urn']['label']

        attr, valt = _mapping.get(label, (label, 'sval'))
        attr = attr.lower()

        if isinstance(prop['value'], dict):
            value = prop['value'].get(valt)

            if value is not None:
                data.append(attr, value)
            else:
                # skip attr as it's not mapped
                hat_geci.append((attr, valt, prop['value']))
        else:
            data.append(attr, prop['value'])

    # merge and transform to standard json
    return dict(data)
