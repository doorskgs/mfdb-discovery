from eme.data_access import get_repo

from metabolite_index import DiscoveryAlg
from metabolite_index.consistency import get_discovery_class, get_discovery_attribute_consistencies, ConsistencyClass
from metabolite_index.dal import ctx, ExternalDBEntity, EDBRepository
from metabolite_index.views.MetaboliteDiscovery import MetaboliteDiscovery
from metabolite_index.edb_formatting.structs import AlmostEqualSet


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
    sess = ctx.get_session()

    repo: EDBRepository = get_repo(ExternalDBEntity)

    for edb_record in repo.list_chebi_iter(stop_at=1000):
        meta = run_discovery(edb_record.edb_source, edb_record.edb_id)

        cmain, cid, cm = get_discovery_class(meta)
        if cmain == ConsistencyClass.Consistent and cid == ConsistencyClass.Consistent:
            mass = AlmostEqualSet(meta.mass).get_set()
            mi_mass = AlmostEqualSet(meta.mi_mass).get_set()

            if len(mass) != 1:
                print(meta.chebi_id,'mass: ', meta.mass, '->', mass)
            if len(mi_mass) != 1:
                print(meta.chebi_id,'mi_mass: ', meta.mi_mass, '->', mi_mass)


if __name__ == "__main__":
    main()
