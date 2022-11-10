import unittest
import random

from metabolite_index.edb_formatting.cluster1d import cluster1d_eps, cluster1d_fixed
from metabolite_index.edb_formatting.structs import AlmostEqualSet


class MassClusteringTests(unittest.TestCase):
    def setUp(self):
        # meth masses:
        mass = [149.23284 , 149.23, 149.2328]
        mi_mass = [149.12045 , 149.120449483 , 149.12044948]

        self.points = mass + mi_mass

    def test_clustering(self):
        # arrange
        random.shuffle(self.points)

        clusters = cluster1d_eps(self.points, eps=0.00005)
        print(clusters)

        self.assertEqual(2, len(clusters))

    def test_almostEqualSet(self):
        # arrange
        random.shuffle(self.points)

        # act
        aes = AlmostEqualSet(self.points)
        actual_repr_set = aes.get_set

        # assert
        expected_repr_set = {149.23284, 149.120449483}
        self.assertEqual(expected_repr_set, actual_repr_set)
