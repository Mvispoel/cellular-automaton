from multiprocessing import Array, Value


class CellState:
    _state_save_slot_count = 2
    """
        This is the base class for all cell states.
        When using the cellular automaton display, inherit this class and implement get_state_draw_color.
    """
    def __init__(self, initial_state=(0., ), draw_first_state=True):
        self._state_slots = [Array('d', initial_state) for i in range(self.__class__._state_save_slot_count)]
        self._active = Value('i', 1)
        self._age = Value('i', 0)
        if draw_first_state:
            self._dirty = Value('i', 1)
        else:
            self._dirty = Value('i', 0)

    def get_age(self):
        return self._age.value

    def get_current_state(self):
        return self.get_state_of_iteration(self.get_age())

    def get_state_of_iteration(self, iteration):
        """ Will return the state for the iteration modulo number of saved states.
        :param iteration:   Uses the iteration index, to differ between concurrent states.
        :return The state for this iteration.
        """
        return self._state_slots[iteration % self.__class__._state_save_slot_count]

    def is_active(self):
        return self._active.value > self._age.value

    def set_active_for_next_iteration(self, iteration):
        self._active.value = max(self._active.value, iteration + 1)

    def increase_age(self):
        with self._age.get_lock():
            self._age.value += 1

    def is_set_for_redraw(self):
        return self._dirty != 1

    def was_redrawn(self):
        self._dirty = 0

    def set_current_state(self, new_state):
        return self.set_state_of_iteration(new_state, self.get_age() + 1)

    def get_state_of_last_iteration(self, current_iteration_index):
        return self.get_state_of_iteration(current_iteration_index - 1)

    def set_state_of_iteration(self, new_state, iteration):
        """ Will set the new state for the iteration modulo number of saved states.
        :param new_state:  The new state to set.
        :param iteration:   Uses the iteration index, to differ between concurrent states.
        :return True if state has changed.
        """

        current_state = self.get_state_of_iteration(iteration)

        changed = False
        for i in range(len(current_state)):
            try:
                if current_state[i] != new_state[i]:
                    changed = True

                current_state[i] = new_state[i]
            except IndexError:
                raise IndexError("New State length or type is invalid!")

        self._dirty.value |= changed
        return changed

    def get_state_draw_color(self, iteration):
        raise NotImplementedError

    def __str__(self):
        return str(self._state_slots)
