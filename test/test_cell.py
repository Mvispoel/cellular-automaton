import sys
sys.path.append('../src')

import cellular_automaton.ca_cell_state as cas
import cellular_automaton.ca_cell as cac
import unittest


class TestState(cas.CellState):
    def __init__(self):
        super().__init__()


class TestCellState(unittest.TestCase):
    def setUp(self):
        self.cell = cac.Cell(TestState, [])
        self.neighbours = [TestState() for x in range(5)]
        for neighbour in self.neighbours:
            neighbour.set_state_of_iteration((0, ), 0)
        self.cell.set_neighbours(self.neighbours)

    def cell_and_neighbours_active(self, iteration):
        self.neighbours.append(self.cell.get_state())
        all_active = True
        for state in self.neighbours:
            if not state.is_active(iteration):
                all_active = False
        return all_active

    def test_evolve_activation(self):
        self.cell.evolve_if_ready((lambda a, b: (1,)), 0)
        all_active = self.cell_and_neighbours_active(1)
        self.assertTrue(all_active)

    def test_evolve_activation_on_no_change(self):
        self.cell.evolve_if_ready((lambda a, b: (0,)), 0)
        all_active = self.cell_and_neighbours_active(1)
        self.assertFalse(all_active)


if __name__ == '__main__':
    unittest.main()
