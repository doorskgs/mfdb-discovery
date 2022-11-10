import json
import math
import time

from eme.data_access import get_repo
from eme.pipe.utils import print_progress

from metabolite_index import DiscoveryAlg
from metabolite_index.consistency import get_discovery_class, ConsistencyClass
from metabolite_index.dal import ctx, ExternalDBEntity, EDBRepository
from metabolite_index.views.MetaboliteDiscovery import MetaboliteDiscovery


def run_discovery(edb_source, edb_id) -> MetaboliteDiscovery:
    disco = DiscoveryAlg()
    disco.verbose = False
    disco.clear()

    meta = MetaboliteDiscovery()
    getattr(meta, edb_source+'_id').add(edb_id)
    disco.add_input(meta, edb_source)

    disco.run_discovery()
    return meta


def main():
    repo: EDBRepository = get_repo(ExternalDBEntity)

    fh1 = open('masses.txt', 'w')
    t=  0
    t1 = time.time()

    for edb_record in repo.list_chebi_iter(stop_at=None):
        meta = run_discovery(edb_record.edb_source, edb_record.edb_id)

        # todo: itt: make table count of inconsistent for all 25k chebi records
        # todo: itt: then try with various clustering algs

        cmain, cid, cm = get_discovery_class(meta)
        if cmain == ConsistencyClass.Consistent and cid == ConsistencyClass.Consistent:
            fh1.write(','.join(list(meta.chebi_id)))
            fh1.write(';')
            json.dump(list(meta.mass), fh1)
            fh1.write(';')
            json.dump(list(meta.mi_mass), fh1)
            fh1.write('\n')

            if t % 1000 == 0:
                print_progress("  {spinner} {iter} [{dt}s]", t, si=(t//1000), tstart=t1)

            t+= 1

    fh1.close()

if __name__ == "__main__":
    main()
