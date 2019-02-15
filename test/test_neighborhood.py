import sys
sys.path.append('../src')

import cellular_automaton.ca_neighborhood as csn
import unittest


class TestNeighborhood(unittest.TestCase):
    @staticmethod
    def check_neighbors(neighborhood, neighborhood_sets):
        for neighborhood_set in neighborhood_sets:
            neighbors = neighborhood.calculate_cell_neighbor_coordinates(neighborhood_set[0], [3, 3])
            if neighborhood_set[1] != neighbors:
                print("Error neighbours do not fit (expected, real): ", (neighborhood_set[1]), neighbors)
                return False
        return True

    def test_ignore_missing_neighbors(self):
        neighborhood = csn.MooreNeighborhood(csn.EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS)
        n00 = [[0, 0], [[1, 0], [0, 1], [1, 1]]]
        n11 = [[1, 1], [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1], [0, 2], [1, 2], [2, 2]]]
        n22 = [[2, 2], [[1, 1], [2, 1], [1, 2]]]
        self.assertTrue(self.check_neighbors(neighborhood, [n00, n11, n22]))

    def test_ignore_edge_cells(self):
        neighborhood = csn.MooreNeighborhood(csn.EdgeRule.IGNORE_EDGE_CELLS)
        n00 = [[0, 0], []]
        n11 = [[1, 1], [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1], [0, 2], [1, 2], [2, 2]]]
        n22 = [[2, 2], []]
        self.assertTrue(self.check_neighbors(neighborhood, [n00, n11, n22]))

    def test_cyclic_dimensions(self):
        neighborhood = csn.MooreNeighborhood(csn.EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
        n00 = [[0, 0], [[2, 2], [0, 2], [1, 2], [2, 0], [1, 0], [2, 1], [0, 1], [1, 1]]]
        n11 = [[1, 1], [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1], [0, 2], [1, 2], [2, 2]]]
        n22 = [[2, 2], [[1, 1], [2, 1], [0, 1], [1, 2], [0, 2], [1, 0], [2, 0], [0, 0]]]
        self.assertTrue(self.check_neighbors(neighborhood, [n00, n11, n22]))


if __name__ == '__main__':
    unittest.main()
