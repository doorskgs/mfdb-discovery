import os.path
import time

from eme.data_access import get_repo

import metabolite_index as mi
from metabolite_index.dal import ExternalDBEntity, EDBRepository


# Configure
path = os.path.dirname(__file__)
disco = mi.discovery(path+'/test_discovery.ini', verbose=False)

repo: EDBRepository = get_repo(ExternalDBEntity)

ndb = 1000
start_db = 16

t1 = time.time()

for edb_id, edb_source in repo.list_iter(stop_at=ndb, start_from=start_db):
    meta = disco.add_scalar_input(mi.EDBSource(edb_source), edb_id)
    disco.run_discovery()

t2 = time.time()

print(f'{ndb} items took', t2 - t1)
