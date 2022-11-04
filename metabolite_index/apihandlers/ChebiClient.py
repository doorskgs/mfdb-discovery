import requests
import xmltodict as xmltodict

from .ApiClientBase import ApiClientBase
from ..attributes import EDB_SOURCES_OTHER, EDB_SOURCES
from ..edb_formatting import pad_id, MultiDict, remap_keys, preprocess, map_to_edb_format
from ..views.MetaboliteConsistent import MetaboliteConsistent


class ChebiClient(ApiClientBase):
    _reverse = (
        'pubchem_id', 'kegg_id', 'hmdb_id', 'lipidmaps_id',
    )
    _mapping = {edb_tag+' accession': edb_tag+'_id' for edb_tag in (EDB_SOURCES|EDB_SOURCES_OTHER)} | \
               {edb_tag+' registry number': edb_tag+'_id' for edb_tag in (EDB_SOURCES|EDB_SOURCES_OTHER)} | \
    {
        'chebiId': 'chebi_id',

        'chebiAsciiName': 'names',
        'Synonyms': 'names',
        'IupacNames': 'names',

        'monoisotopicMass': 'mi_mass',
        'entityStar': 'stars',
        'Formulae': 'formula',

        'SecondaryChEBIIds': 'chebi_id_alt',
        'wikipedia accession': 'wiki_id',
        'kegg compound accession': 'kegg_id',
    }

    _important_attr = {
        'stars'
    }

    def fetch_api(self, edb_id):
        edb_id = pad_id(edb_id, "chebi_id")
        url = f'https://www.ebi.ac.uk/webservices/chebi/2.0/test/getCompleteEntity?chebiId={edb_id}'
        r = requests.get(url=url)

        data = MultiDict()

        resp = xmltodict.parse(r.text)
        resp = resp['S:Envelope']['S:Body']['getCompleteEntityResponse']['return']

        # add DatabaseLinks as refs
        for oof in resp.pop('DatabaseLinks') + resp.pop('RegistryNumbers'):
            data.append(oof['type'].lower(), oof['data'])

        for k,v in resp.items():
            if isinstance(v, list) and isinstance(v[0], dict):
                if 'data' in v[0]:
                    # flatten list of dicts
                    for el in v:
                        data.append(k, el['data'])
                else:
                    # OnthologyParents, ChemicalStructures, OnthologyChildren, CompoundOrigins
                    # skipped for now
                    pass
            elif isinstance(v, dict):
                if 'data' in v:
                    data.append(k, v['data'])
                else:
                    print('???', v)
            else:
                data.append(k, v)

        remap_keys(data, self._mapping)
        preprocess(data)
        data, etc = map_to_edb_format(data, important_attr=self._important_attr, edb_format=None, exclude_etc={None})

        data['edb_source'] = 'chebi'
        return MetaboliteConsistent(**data)

# 'definition': '',
# 'status': '',
# 'smiles': '',
# 'inchi': '',
# 'inchiKey': '',
# 'charge': '',
# 'mass': '',
# 'RegistryNumbers': '',
# 'Citations': '',
# 'ChemicalStructures': '',
# 'DatabaseLinks': '',
# 'OntologyParents': '',
# 'OntologyChildren': '',
# 'CompoundOrigins': ''
