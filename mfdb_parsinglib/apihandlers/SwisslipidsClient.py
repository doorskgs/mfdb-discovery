from .ApiClientBase import ApiClientBase


class SwisslipidsClient(ApiClientBase):
    def __init__(self):
        super().__init__()

        #self.load_mapping('swisslipids')

    def fetch_api(self, edb_id):
        print("Not Implemented:", self.__class__.__name__)

        return None
