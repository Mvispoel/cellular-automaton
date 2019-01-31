import sys
sys.path.append('../src')

import cellular_automaton.ca_cell_state as cs
import unittest


class TestCellState(unittest.TestCase):

    def test_get_state_of_iteration(self):
        cell_state = cs.CellState(0, state_save_slot_count=3)
        cell_state.set_status_of_iteration(1, 0)
        self.assertEqual(cell_state.get_status_of_iteration(3), 1)

    def test_set_state_applies_overflow(self):
        cell_state = cs.CellState(0, state_save_slot_count=4)
        cell_state.set_status_of_iteration(1, 4)
        self.assertEqual(cell_state.get_status_of_iteration(0), 1)

    def test_set_state_only_applies_to_iteration_slot(self):
        cell_state = cs.CellState(0, state_save_slot_count=2)
        cell_state.set_status_of_iteration(1, 0)
        self.assertEqual(cell_state.get_status_of_iteration(1), 0)


if __name__ == '__main__':
    unittest.main()
