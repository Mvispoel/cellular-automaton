class CellState:
    """
        This is the base class for all cell states.
        When using the cellular automaton display, inherit this class and implement get_state_draw_color.
    """
    def __init__(self, initial_state):
        self._state = [[initial_state], [initial_state]]

    def set_status_of_iteration(self, new_status, iteration):
        """ Will set the new status for the iteration modulo two.
        :param new_status:  The new status to set.
        :param iteration:   Uses the iteration index, to differ between current and next state.
        :return True if status has changed.
        """
        self._state[iteration % 2] = new_status

        return self._state[0] != self._state[1]

    def get_status_of_iteration(self, iteration):
        """ Will return the status for the iteration modulo two.
        :param iteration:   Uses the iteration index, to differ between current and next state.
        :return The status for this iteration.
        """
        return self._state[iteration % 2]

    def get_state_draw_color(self, iteration):
        raise NotImplementedError
