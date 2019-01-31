from multiprocessing import Array, Value


class CellState:
    """
        This is the base class for all cell states.
        When using the cellular automaton display, inherit this class and implement get_state_draw_color.
    """
    def __init__(self, initial_state=(0., ), state_save_slot_count=2, draw_first_state=True):
        self._state_save_slot_count = state_save_slot_count
        self._state_slots = [Array('d', initial_state)] * state_save_slot_count
        if draw_first_state:
            self._dirty = Value('i', 1)
        else:
            self._dirty = Value('i', 0)

    def is_set_for_redraw(self):
        return self._dirty != 1

    def get_state_changes(self):
        return self._dirty

    def set_for_redraw(self):
        self._dirty = 1

    def was_redrawn(self):
        self._dirty = 0

    def set_current_state(self, new_state, current_iteration_index):
        return self.set_state_of_iteration(new_state, current_iteration_index)

    def get_state_of_last_iteration(self, current_iteration_index):
        return self.get_state_of_iteration(current_iteration_index - 1)

    def set_state_of_iteration(self, new_state, iteration):
        """ Will set the new state for the iteration modulo number of saved states.
        :param new_state:  The new state to set.
        :param iteration:   Uses the iteration index, to differ between concurrent states.
        :return True if state has changed.
        """
        slot_count = self._state_save_slot_count
        states = self._state_slots

        current_state = states[iteration % slot_count]

        changed = False
        for i in range(len(current_state)):
            try:
                if current_state[i] != new_state[i]:
                    changed = True

                current_state[i] = new_state[i]
            except IndexError:
                raise IndexError("New State length or type is invalid!")

        self._dirty |= changed
        return changed

    def get_state_of_iteration(self, iteration):
        """ Will return the state for the iteration modulo number of saved states.
        :param iteration:   Uses the iteration index, to differ between concurrent states.
        :return The state for this iteration.
        """
        return self._state_slots[iteration % self._state_save_slot_count]

    def get_state_draw_color(self, iteration):
        raise NotImplementedError

    def __str__(self):
        return str(self._state_slots)
