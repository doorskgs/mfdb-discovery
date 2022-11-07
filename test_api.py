from metabolite_index.apihandlers.LipidmapsClient import LipidmapsClient
from metabolite_index.apihandlers.ChebiClient import ChebiClient
from metabolite_index.apihandlers.PubchemClient import PubchemClient
from metabolite_index.apihandlers.HMDBClient import HMDBClient


lm_cholesterol = 'LMST01010001'
pc_cholesterol = '5997'
hmdb_cholesterol = 'HMDB0000067'

api_lm = LipidmapsClient()
api_pc = PubchemClient()
api_hmdb = HMDBClient()

# --------------------------------------------

resp = api_hmdb.fetch_api(hmdb_cholesterol)

print(resp)
