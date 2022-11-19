import requests

from io import StringIO, BytesIO
import xml.etree.ElementTree as ET

from lxml import etree

from .ApiClientBase import ApiClientBase
from ..edb_formatting import pad_id, preprocess, remap_keys, map_to_edb_format, replace_obvious_hmdb_id, MultiDict
from ..dal import ExternalDBEntity


class HMDBClient(ApiClientBase):
    _reverse = (
        'pubchem_id', 'kegg_id', 'chebi_id',
    )

    _mapping = {
        'accession': 'hmdb_id',

        'name': 'names',
        'iupac_name': 'names',
        'synonyms': 'names',
        'traditional_iupac': 'names',

        'formal_charge': 'charge',
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

    explore_children = {'secondary_accessions','synonyms'}

    def fetch_api(self, edb_id):
        db_id = pad_id(edb_id, 'hmdb_id')
        r = requests.get(url=f'https://hmdb.ca/metabolites/{db_id}.xml', allow_redirects=False)

        if r.is_redirect or r.status_code == 301:
            # we queried a secondary ID, follow the redirect of the api
            next_url = r.next.url+'.xml'
            print("  HMDB: redirecting to", next_url)
            r = requests.get(url=next_url)

        is_xml = r.headers['content-type'].startswith('application/xml')
        if r.status_code != 200 and r.status_code != 304 or r.content is None or is_xml:
            return None

        #xmlns = 'http://www.hmdb.ca'
        #filter_tag = f'{{{xmlns}}}metabolite'
        filter_tag = 'metabolite'

        context = etree.iterparse(BytesIO(r.content), events=('end',), tag=filter_tag)
        context = iter(context)
        _xevt, xmeta = next(context)

        data = MultiDict()

        # parse lxml's hierarchy into a dictionary
        for tag in xmeta:
            tag_name = tag.tag#.removeprefix('{' + xmlns + '}')

            if len(tag) == 0:
                data.append(tag_name, tag.text)
            else:
                if tag_name in self.explore_children:
                    for child in tag:
                        # assert len(child) == 0
                        data.append(tag_name, child.text)
        xmeta.clear(keep_tail=False)

        remap_keys(data, self._mapping)
        preprocess(data)
        data, etc = map_to_edb_format(data, important_attr=self._important_attr)

        data['edb_source'] = 'hmdb'
        return ExternalDBEntity(**data)
