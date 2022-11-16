import os.path

import metabolite_index as mi

"""
MFDB-Discovery has convenience methods to configure the algorithm in another package

"""

# Configure
path = os.path.dirname(__file__)
disco = mi.discovery(path+'/test_discovery.ini', verbose=True)

# run
meta = disco.add_scalar_input(mi.EDBSource.chebi, 'CHEBI:40938')
disco.run_discovery()

# evaluate
c_master_ids, c_edb_ids, c_mass = mi.get_consistency_class(meta)
print(c_master_ids, c_edb_ids, c_mass)
print(repr(meta))
print("Found 2nd IDs:", disco.secondary_ids)
print("Discovered:", disco.discovered)
print("Undiscovered:", disco.undiscovered)
print("Ambiguous:", disco.ambiguous)
