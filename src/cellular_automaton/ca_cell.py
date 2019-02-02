from cellular_automaton.ca_cell_state import CellState


class Cell:
    def __init__(self, state_class: CellState.__class__, coordinate: list):
        self._coordinate = coordinate
        self._state = state_class()
        self._neighbours = []

    def set_neighbours(self, neighbours):
        self._neighbours = neighbours

    def get_state(self):
        return self._state

    def get_coordinate(self):
        return self._coordinate

    def evolve_if_ready(self, rule):
        if self._neighbours_are_younger():
            if self._state.is_active():
                new_state = rule(self._state.get_current_state(), self.get_neighbour_states())
                self.set_new_state_and_activate(new_state)

            self._state.increase_age()

    def _neighbours_are_younger(self):
        for n in self._neighbours:
            if n.get_age() < self._state.get_age():
                return False
        return True

    def get_neighbour_states(self):
        return [n.get_state_of_iteration(self._state.get_age()) for n in self._neighbours]

    def set_new_state_and_activate(self, new_state: CellState):
        changed = self._state.set_current_state(new_state)
        if changed:
            self._set_active()

    def _set_active(self):
        self._state.set_active_for_next_iteration(self._state.get_age() + 1)
        for n in self._neighbours:
            n.set_active_for_next_iteration(self._state.get_age() + 1)
