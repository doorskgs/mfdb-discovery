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
meta.chebi_id.add('CHEBI:15422')
disco.add_input(meta, mi.EDBSource.hmdb)

# run
disco.run_discovery()

print(repr(meta))
