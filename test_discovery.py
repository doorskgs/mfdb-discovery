import asyncio
import os.path

import mfdb_parsinglib as mi
import mfdb_parsinglib.consistency as cons

"""
MFDB-Discovery has convenience methods to configure the algorithm in another package

"""

# Configure
path = os.path.dirname(__file__)
disco = mi.discovery(path+'/test_discovery.ini', verbose=True)

async def main():
    await disco.mgr.initialize()

    # run
    meta = disco.add_scalar_input(mi.EDBSource.pubchem, '101054762')
    await disco.run_discovery()

    # evaluate
    c_master_ids, c_edb_ids, c_mass = cons.get_consistency_class(meta)

    print(repr(meta))
    print("Master ID consistency: ", c_master_ids)
    print("EDB ID consistency: ", c_edb_ids)
    print("Mass Consistency: ", c_mass)

    print("Found 2nd IDs:", disco.secondary_ids)
    print("Discovered:", disco.discovered)
    print("Undiscovered:", disco.undiscovered)
    print("Ambiguous:", disco.ambiguous)

if __name__=="__main__":
    asyncio.run(main())
