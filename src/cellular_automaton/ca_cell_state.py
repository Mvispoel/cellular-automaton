from multiprocessing import RawArray, RawValue
from ctypes import c_float, c_bool


class CellState:
    _state_save_slot_count = 2
    """
        This is the base class for all cell states.
        When using the cellular automaton display, inherit this class and implement get_state_draw_color.
    """
    def __init__(self, initial_state=(0., ), draw_first_state=True):
        self._state_slots = [RawArray(c_float, initial_state) for i in range(self.__class__._state_save_slot_count)]
        self._active = [RawValue(c_bool, False) for i in range(self.__class__._state_save_slot_count)]
        self._active[0].value = True
        if draw_first_state:
            self._dirty = RawValue(c_bool, True)
        else:
            self._dirty = RawValue(c_bool, False)

    def is_active(self, iteration):
        return self._active[self.__calculate_slot(iteration)]

    def set_active_for_next_iteration(self, iteration):
        self._active[self.__calculate_slot(iteration + 1)].value = True

    def is_set_for_redraw(self):
        return self._dirty.value

    def was_redrawn(self):
        self._dirty.value = False

    def get_state_of_last_iteration(self, current_iteration_index):
        return self.get_state_of_iteration(current_iteration_index - 1)

    def get_state_of_iteration(self, iteration):
        """ Will return the state for the iteration modulo number of saved states.
        :param iteration:   Uses the iteration index, to differ between concurrent states.
        :return The state for this iteration.
        """
        return self._state_slots[self.__calculate_slot(iteration)]

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
        self._active[self.__calculate_slot(iteration)].value = False
        return changed

    def get_state_draw_color(self, iteration):
        raise NotImplementedError

    @classmethod
    def __calculate_slot(cls, iteration):
        return iteration % cls._state_save_slot_count
