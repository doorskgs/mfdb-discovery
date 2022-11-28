from .views.MetaboliteDiscovery import MetaboliteDiscovery
from .views.MetaboliteConsistent import MetaboliteConsistent

from .attributes import EDB_SOURCES, EDB_SOURCES_OTHER, EDB_ID, EDB_ID_OTHER, COMMON_ATTRIBUTES, EDBSource

from .setup import build_discovery as discovery
from .DiscoveryAlg import DiscoveryAlg

# import mappings as well
from .mapping import consistent2disco

def get_mdb_id(mdb: dict | MetaboliteDiscovery | MetaboliteConsistent, level=4):
    primary_ids = []

    if isinstance(mdb, dict):
        primary_ids.append(mdb['inchikey'])
        primary_ids.append(mdb['chebi_id'])
        primary_ids.append(mdb['pubchem_id'])
        primary_ids.append(mdb['hmdb_id'])
    else:
        primary_ids.append(mdb.inchikey)
        primary_ids.append(mdb.chebi_id)
        primary_ids.append(mdb.pubchem_id)
        primary_ids.append(mdb.hmdb_id)

    for i in range(level):
        primary_id = primary_ids[i]
        if not isinstance(primary_id, (set, list, tuple)):
            value = primary_id
        elif not primary_id:
            value = None
        else:
            value = next(iter(primary_id))

        if value is not None:
            return value
    return None


__all__ = [
    'discovery', 'get_mdb_id',
    'EDBSource', 'EDB_SOURCES', 'EDB_ID', 'EDB_ID_OTHER', 'COMMON_ATTRIBUTES',
    'MetaboliteDiscovery'
]
