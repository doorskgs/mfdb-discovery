from metabolite_index.apihandlers.ChebiClient import ChebiClient

api = ChebiClient()

resp = api.fetch_api('CHEBI:15422')

print(resp)