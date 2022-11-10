from collections import defaultdict

import requests

from .ApiClientBase import ApiClientBase
from ..edb_formatting import preprocess, map_to_edb_format, remap_keys, MultiDict
from ..views.MetaboliteConsistent import MetaboliteConsistent


class PubchemClient(ApiClientBase):
    _reverse = (
        'chebi_id', 'hmdb_id', 'kegg_id'
    )
    _mapping = {
        #'InChIKey': ('inchikey', 'sval'),
        #'InChI': ('inchi', 'sval'),

        'IUPAC Name': ('names', 'sval'),
        'Molecular Formula': ('formula', 'sval'),

        'Molecular Weight': ('mass', 'fval'),
        'Mass': ('mi_mass', 'fval'),
        'Log P': ('logp', 'fval'),
    }

    _important_attr = {
        'logp'
    }

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
        data, etc = map_to_edb_format(data, important_attr=self._important_attr, edb_format=None, exclude_etc={None})

        data['edb_source'] = 'pubchem'
        return MetaboliteConsistent(**data)


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

        if 'ebi.ac.uk/chebi' in link:
            # http://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:18102
            db_id = link.split('chebiid=chebi:')[1].upper()
            data.append('chebi_id', db_id)
        elif 'chemspider.com' in link:
            # http://www.chemspider.com/Chemical-Structure.10128115.html
            db_id = link.split('.')[-2]
            data.append('chemspider_id', db_id)
        elif 'lipidmaps.org' in link:
            # http://www.lipidmaps.org/data/LMSDRecord.php?LM_ID=LMFA07070002
            db_id = link.lower().split('lm_id=')[1].upper()
            data.append('lipmaps_id', db_id)
        elif 'hmdb.ca' in link:
            # http://www.hmdb.ca/metabolites/HMDB0000791
            db_id = link.split('metabolites/')[1].upper()
            data.append('hmdb_id', db_id)
        else:
            # unrecognized XREF
            continue

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
