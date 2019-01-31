import sys
sys.path.append('../src')

import cellular_automaton.ca_cell_state as cs
import unittest


class TestState(unittest.TestCase):

    def test_state_slots(self):
        cell_state = cs.CellState([0])
        cell_state.set_status_of_iteration([1], 0)
        cell_state.set_status_of_iteration([2], 1)
        cell_state.set_status_of_iteration([3], 2)

        self.assertEqual(cell_state.get_status_of_iteration(0), [3])


if __name__ == '__main__':
    unittest.main()
