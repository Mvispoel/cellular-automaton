import sys
sys.path.append('../src')

from cellular_automaton import *
import unittest
import mock


class TestFac(CAFactory):
    @staticmethod
    def make_cells(dimension, state_class):
        return CAFactory._make_cells(dimension, state_class)

    @staticmethod
    def apply_neighbourhood(cells, neighborhood, dimension):
        return CAFactory._apply_neighbourhood_to_cells(cells, neighborhood, dimension)


class TestCAFactory(unittest.TestCase):
    def test_make_ca_calls_correct_methods(self):
        with mock.patch.object(CAFactory, '_make_cells', return_value={1: True}) as m1:
            with mock.patch.object(CAFactory, '_apply_neighbourhood_to_cells') as m2:
                CAFactory.make_cellular_automaton([10], Neighborhood, CellState)
                m1.assert_called_once_with([10], CellState)
                m2.assert_called_once_with({1: True}, Neighborhood, [10])

    def test_make_ca_returns_correct_values(self):
        with mock.patch.object(CAFactory, '_make_cells', return_value={1: True}):
            with mock.patch.object(CAFactory, '_apply_neighbourhood_to_cells'):
                cells = CAFactory.make_cellular_automaton([10], Neighborhood, CellState)
                self.assertEqual(tuple(cells.values()), (True, ))

    def test_1dimension_coordinates(self):
        fac = TestFac()
        c = fac.make_cells([3], CellState)
        self.assertEqual(list(c.keys()), [(0,), (1,), (2,)])

    def test_2dimension_coordinates(self):
        fac = TestFac()
        c = fac.make_cells([2, 2], CellState)
        self.assertEqual(list(c.keys()), [(0, 0), (0, 1), (1, 0), (1, 1)])

    def test_3dimension_coordinates(self):
        fac = TestFac()
        c = fac.make_cells([2, 2, 2], CellState)
        self.assertEqual(list(c.keys()), [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
                                          (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)])

    def test_apply_neighbourhood(self):
        fac = TestFac()
        cells = fac.make_cells([3, 3], CellState)
        fac.apply_neighbourhood(cells, MooreNeighborhood(EdgeRule.IGNORE_EDGE_CELLS), [3, 3])

        neighbours = self.__create_neighbour_list_of_cell((1, 1), cells)

        self.assertEqual(set(neighbours), set(cells[(1, 1)].neighbours))

    @staticmethod
    def __create_neighbour_list_of_cell(cell_id, cells):
        neighbours = []
        for c in cells.values():
            if c != cells[cell_id]:
                neighbours.append(c.state)
        return neighbours


if __name__ == '__main__':
    unittest.main()
