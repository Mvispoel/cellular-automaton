import multiprocessing

from cellular_automaton.ca_cell_state import CellState


class Cell:
    def __init__(self, name, state_class: CellState.__class__, coordinate: list):
        self._name = name
        self._coordinate = coordinate
        self._state = state_class()
        self._neighbours = []
        self._active = multiprocessing.Value('i', 1)
        self._age = multiprocessing.Value('i', 0)

    def set_neighbours(self, neighbours):
        self._neighbours = neighbours

    def get_coordinate(self):
        return self._coordinate

    def evolve_if_ready(self, rule):
        if self._neighbours_are_younger():
            if self._is_active():
                new_state = rule(self.get_current_state(), self.get_neighbour_states())
                self.set_new_state_and_activate(new_state)

            self.increase_age()

    def _neighbours_are_younger(self):
        for n in self._neighbours:
            if n.get_age() < self.get_age():
                return False

    def get_age(self):
        return self._age.value

    def _is_active(self):
        return self._active.value > self._age.value

    def get_current_state(self):
        return self._state.get_state_of_iteration(self._age.value)

    def get_neighbour_states(self):
        return [n.get_state_from_iteration(self._age.value) for n in self._neighbours]

    def set_new_state_and_activate(self, new_state: CellState):
        changed = self._state.set_current_state(new_state, self._age.value + 1)
        if changed:
            self._set_active()

    def _set_active(self):
        self.set_active_for_next_iteration(self._age.value)
        for n in self._neighbours:
            n.set_active_for_next_iteration(self._age.value)

    def set_active_for_next_iteration(self, iteration):
        self._active.value = max(self._active.value, iteration + 1)

    def increase_age(self):
        with self._age.get_lock():
            self._age += 1
