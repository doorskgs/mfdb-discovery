import requests

from .ApiClientBase import ApiClientBase
from metabolite_index.edb_formatting import pad_id


class HMDBClient(ApiClientBase):
    _reverse = (
        'pubchem_id', 'kegg_id', 'chebi_id',
    )
    def fetch_api(self, edb_id):
        print("Not Implemented:", self.__class__.__name__)
        db_id = pad_id(edb_id, 'hmdb_id')
        r = requests.get(url=f'http://www.hmdb.ca/metabolites/{db_id}.xml')

        if r.status_code != 200 and r.status_code != 304:
            return None

        print(1)
        return None
        # data: HMDBData = parse_hmdb_api(r.content)
        #
        # return self.to_view(data) if meta_view else data
