import sys
sys.path.append('../src')

from cellular_automaton import *
import unittest


class TestState(CellState):
    def __init__(self):
        super().__init__()


class TestCellState(unittest.TestCase):
    def setUp(self):
        self.cell = [TestState(), []]
        self.neighbours = [TestState() for x in range(5)]
        for neighbour in self.neighbours:
            neighbour.set_state_of_iteration((0, ), 0)
        self.cell[1] = self.neighbours

    def cell_and_neighbours_active(self, iteration):
        self.neighbours.append(self.cell[0])
        all_active = True
        for state in self.neighbours:
            if not state.is_active(iteration):
                all_active = False
        return all_active

    def test_evolve_activation(self):
        Cell.evolve_if_ready(self.cell, (lambda a, b: (1,)), 0)
        all_active = self.cell_and_neighbours_active(1)
        self.assertTrue(all_active)

    def test_evolve_activation_on_no_change(self):
        Cell.evolve_if_ready(self.cell, (lambda a, b: (0,)), 0)
        all_active = self.cell_and_neighbours_active(1)
        self.assertFalse(all_active)


if __name__ == '__main__':
    unittest.main()
