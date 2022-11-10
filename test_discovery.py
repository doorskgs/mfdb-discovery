import metabolite_index as mi

"""
MFDB-Discovery has convenience methods to configure the algorithm in another package

"""

# Configure
disco = mi.DiscoveryAlg()
disco.verbose = True

# ATP
disco.clear()
meta = mi.MetaboliteDiscovery()
meta.chebi_id.add('CHEBI:185024')
disco.add_input(meta, mi.EDBSource.hmdb)

# run
disco.run_discovery()

c_master_ids, c_edb_ids, c_mass = mi.get_discovery_class(meta)

print(c_master_ids, c_edb_ids, c_mass)
print(repr(meta))
