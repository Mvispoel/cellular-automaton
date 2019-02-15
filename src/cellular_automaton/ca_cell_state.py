from multiprocessing import RawArray, RawValue
from ctypes import c_float, c_bool


class CellState:
    """
        This is the base class for all cell states.
        When using the cellular automaton display, inherit this class and implement get_state_draw_color.
    """

    _state_save_slot_count = 2

    def __init__(self, initial_state=(0., ), draw_first_state=True):
        self._state_slots = [list(initial_state) for i in range(self.__class__._state_save_slot_count)]
        self._active = [False for i in range(self.__class__._state_save_slot_count)]
        self._active[0] = True
        self._dirty = draw_first_state

    def is_active(self, iteration):
        return self._active[self._calculate_slot(iteration)]

    def set_active_for_next_iteration(self, iteration):
        self._active[self._calculate_slot(iteration + 1)] = True

    def is_set_for_redraw(self):
        return self._dirty

    def was_redrawn(self):
        self._dirty = False

    def get_state_of_last_iteration(self, current_iteration_index):
        return self.get_state_of_iteration(current_iteration_index - 1)

    def get_state_of_iteration(self, iteration):
        """ Will return the state for the iteration modulo number of saved states.
        :param iteration:   Uses the iteration index, to differ between concurrent states.
        :return The state for this iteration.
        """
        return self._state_slots[self._calculate_slot(iteration)]

    def set_state_of_iteration(self, new_state, iteration):
        """ Will set the new state for the iteration modulo number of saved states.
        :param new_state:  The new state to set.
        :param iteration:  Uses the iteration index, to differ between concurrent states.
        :return True if state has changed.
        """
        self._change_state_values(new_state, iteration)
        changed = self._did_state_change(iteration)
        self._dirty |= changed
        self._active[self._calculate_slot(iteration)] = False

        return changed

    def _did_state_change(self, iteration):
        for a, b in zip(self._state_slots[self._calculate_slot(iteration)],
                        self._state_slots[self._calculate_slot(iteration - 1)]):
            if a != b:
                return True
        return False

    def _change_state_values(self, new_state, iteration):
        current_state = self.get_state_of_iteration(iteration)
        if len(new_state) != len(current_state):
            raise IndexError("State length may not change!")

        for i, ns in enumerate(new_state):
                if current_state[i] != ns:
                    current_state[i] = ns

    def get_state_draw_color(self, iteration):
        raise NotImplementedError

    @classmethod
    def _calculate_slot(cls, iteration):
        return iteration % cls._state_save_slot_count


class SynchronousCellState(CellState):
    """
        CellState version using shared values for multi processing purpose.
    """
    def __init__(self, initial_state=(0., ), draw_first_state=True):
        super().__init__(initial_state, draw_first_state)
        self._state_slots = [RawArray(c_float, initial_state) for i in range(self.__class__._state_save_slot_count)]
        self._active = [RawValue(c_bool, False) for i in range(self.__class__._state_save_slot_count)]
        self._active[0].value = True
        self._dirty = RawValue(c_bool, draw_first_state)

    def set_active_for_next_iteration(self, iteration):
        self._active[self._calculate_slot(iteration + 1)].value = True

    def is_set_for_redraw(self):
        return self._dirty.value

    def was_redrawn(self):
        self._dirty.value = False

    def set_state_of_iteration(self, new_state, iteration):
        self._change_state_values(new_state, iteration)
        changed = self._did_state_change(iteration)
        self._dirty.value |= changed
        self._active[self._calculate_slot(iteration)].value = False
        return changed

    @classmethod
    def _calculate_slot(cls, iteration):
        return iteration % cls._state_save_slot_count
