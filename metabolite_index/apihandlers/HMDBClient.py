import requests
from io import StringIO, BytesIO
import xml.etree.ElementTree as ET

from .ApiClientBase import ApiClientBase
from ..edb_formatting import pad_id, preprocess, remap_keys, map_to_edb_format
from ..views.MetaboliteConsistent import MetaboliteConsistent


class HMDBClient(ApiClientBase):
    _reverse = (
        'pubchem_id', 'kegg_id', 'chebi_id',
    )

    _mapping = {
        'accession': 'hmdb_id',

        'name': 'names',
        'iupac_name': 'names',
        'traditional_iupac': 'names',

        'average_molecular_weight': 'mass',
        'avg_mol_weight': 'mass',
        'monoisotopic_molecular_weight': 'mi_mass',
        'monoisotopic_mol_weight': 'mi_mass',
        'monisotopic_molecular_weight': 'mi_mass',
        'monisotopic_mol_weight': 'mi_mass',
        'chemical_formula': 'formula',
        'smiles': 'smiles',
        'inchi': 'inchi',
        'inchikey': 'inchikey',

        'cas_registry_number': 'cas_id',
        'pubchem_compound_id': 'pubchem_id',
        'wikipedia_id': 'wiki_id',
    }

    _important_attr = {
        'state'
    }

    def fetch_api(self, edb_id):
        db_id = pad_id(edb_id, 'hmdb_id')
        r = requests.get(url=f'http://www.hmdb.ca/metabolites/{db_id}.xml')

        if r.status_code != 200 and r.status_code != 304 or r.content is None:
            return None

        context = ET.iterparse(BytesIO(r.content), events=("start", "end"))
        context = iter(context)

        _xevt, xmeta = next(context)

        raise NotImplementedError("copy from DB Builder new HMDB shiet")

        data = parse_xml_recursive(context, has_xmlns=False)

        if isinstance(data, str) or data is None:
            return None

        flatten_hmdb_hierarchies2(data)
        remap_keys(data, self._mapping)
        preprocess(data)
        data, etc = map_to_edb_format(data, important_attr=self._important_attr)

        data['edb_source'] = 'hmdb'
        return MetaboliteConsistent(**data)
