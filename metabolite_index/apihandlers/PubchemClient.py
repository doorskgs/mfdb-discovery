import requests

from .ApiClientBase import ApiClientBase


class PubchemClient(ApiClientBase):
    _reverse = (
        'chebi_id', 'hmdb_id', 'kegg_id'
    )
    def fetch_api(self, edb_id):
        return None
        print("Not Implemented:", self.__class__.__name__)
        r = requests.get(url=f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{edb_id}/json')
        r2 = requests.get(url=f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{edb_id}/xrefs/SBURL/json')

        # todo: description, synonyms, services

        s1 = r.status_code
        s2 = r2.status_code

        if (s1 != 200 and s1 != 304) or (s2 != 200 and s2 != 304):
            return None

        data = parse_pubchem(edb_id, r.text, r2.text)

        return self.to_view(data) if meta_view else data
