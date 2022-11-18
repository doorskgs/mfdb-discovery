import requests

from .ApiClientBase import ApiClientBase
from ..edb_formatting import pad_id, remap_keys, preprocess, map_to_edb_format
from ..dal import ExternalDBEntity


class LipidmapsClient(ApiClientBase):
    _mapping = {

    }

    _important_attr = {
        ''
    }

    def fetch_api(self, edb_id):
        url = f'https://www.lipidmaps.org/rest/compound/lm_id/{pad_id(edb_id, "lipmaps_id")}/all/'
        r = requests.get(url=url)

        data = r.json()

        remap_keys(data, self._mapping)
        preprocess(data)
        data, etc = map_to_edb_format(data, important_attr=self._important_attr, edb_format=None, exclude_etc={None})

        data['edb_source'] = 'lipmaps'
        return ExternalDBEntity(**data)
