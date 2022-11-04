import requests

from .ApiClientBase import ApiClientBase
from metabolite_index.edb_formatting import pad_id

class LipidmapsClient(ApiClientBase):

    def fetch_api(self, edb_id):
        url = f'https://www.lipidmaps.org/rest/compound/lm_id/{pad_id(db_id, "lipidmaps_id")}/all/'
        r = requests.get(url=url)

        data = parse_lipidmaps(r.text)

        return self.to_view(data) if meta_view else data
