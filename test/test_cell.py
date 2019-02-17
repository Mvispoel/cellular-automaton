import sys
sys.path.append('../src')

from cellular_automaton.cellular_automaton import *
import unittest


class TestState(CellState):
    def __init__(self):
        super().__init__()


class TestCellState(unittest.TestCase):
    def setUp(self):
        self.cell = Cell(TestState)
        self.neighbors = [TestState() for x in range(5)]
        for neighbor in self.neighbors:
            neighbor.set_state_of_evolution_step((0, ), 0)
        self.cell.neighbor_states = self.neighbors

    def cell_and_neighbors_active(self, evolution_step):
        self.neighbors.append(self.cell.state)
        all_active = True
        for state in self.neighbors:
            if not state.is_active(evolution_step):
                all_active = False
        return all_active

    def test_evolve_activation(self):
        self.cell.evolve_if_ready((lambda a, b: (1,)), 0)
        all_active = self.cell_and_neighbors_active(1)
        self.assertTrue(all_active)

    def test_evolve_activation_on_no_change(self):
        self.cell.evolve_if_ready((lambda a, b: (0,)), 0)
        all_active = self.cell_and_neighbors_active(1)
        self.assertFalse(all_active)


if __name__ == '__main__':
    unittest.main()
