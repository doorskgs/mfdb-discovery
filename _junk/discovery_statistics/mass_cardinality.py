import json
import math
import time
from collections import defaultdict
import tabulate

from eme.pipe.utils import print_progress

from metabolite_index.edb_formatting.cluster1d import get_digits, get_common_min_precision
from metabolite_index.edb_formatting.structs import AlmostEqualSet


def main():
    total = 0
    cosistent_mass = 0
    t1 = time.time()

    table = []

    with open('masses.txt') as fh:
        for line in fh:
            s = line.split(';')
            chebi_id = s.pop(0)
            masses, mi_masses = map(json.loads, s)

            aes_mass = AlmostEqualSet(masses).equivalence_set
            aes_mass_mi = AlmostEqualSet(mi_masses).equivalence_set

            if len(aes_mass) != 1 or len(aes_mass_mi) != 1:
                table.append([chebi_id, masses, aes_mass, mi_masses, aes_mass_mi])
            else:
                cosistent_mass += 1

            total += 1

    print("")
    print(f"Both masses consistent: {cosistent_mass} / {total}")
    print("\n")
    print(tabulate.tabulate(table, headers=('chebi_id', 'mass', 'equ set', 'mi mass', 'mi equ set')))


if __name__ == "__main__":
    main()
