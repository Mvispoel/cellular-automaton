class CellState:
    """
        This is the base class for all cell states.
        When using the cellular automaton display, inherit this class and implement get_state_draw_color.
    """
    def __init__(self, initial_state, state_save_slot_count=2):
        self._state_save_slot_count = state_save_slot_count
        self._state_slots = [initial_state] * state_save_slot_count

    def set_status_of_iteration(self, new_status, iteration):
        """ Will set the new status for the iteration modulo number of saved states.
        :param new_status:  The new status to set.
        :param iteration:   Uses the iteration index, to differ between concurrent states.
        :return True if status has changed.
        """
        slot_count = self._state_save_slot_count
        states = self._state_slots

        states[iteration % slot_count] = new_status

        return states[(iteration - 1) % slot_count] \
            != states[iteration % slot_count]

    def get_status_of_iteration(self, iteration):
        """ Will return the status for the iteration modulo number of saved states.
        :param iteration:   Uses the iteration index, to differ between concurrent states.
        :return The status for this iteration.
        """
        return self._state_slots[iteration % self._state_save_slot_count]

    def get_state_draw_color(self, iteration):
        raise NotImplementedError

    def __str__(self):
        return str(self._state_slots)
