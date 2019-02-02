import sys
sys.path.append('../src')

import cellular_automaton.ca_cell_state as cs
import unittest


class TestCellState(unittest.TestCase):

    def test_get_state_with_overflow(self):
        cell_state = cs.CellState(initial_state=(0,))
        cell_state.set_state_of_iteration(new_state=(1,), iteration=0)
        self.assertEqual(tuple(cell_state.get_state_of_iteration(2)), (1,))

    def test_set_state_with_overflow(self):
        cell_state = cs.CellState(initial_state=(0,))
        cell_state.set_state_of_iteration(new_state=(1,), iteration=2)
        self.assertEqual(tuple(cell_state.get_state_of_iteration(0)), (1,))

    def test_set_state_does_not_effect_all_slots(self):
        cell_state = cs.CellState(initial_state=(0,))
        cell_state.set_state_of_iteration(new_state=(1,), iteration=0)
        self.assertEqual(tuple(cell_state.get_state_of_iteration(1)), (0,))


if __name__ == '__main__':
    unittest.main()
