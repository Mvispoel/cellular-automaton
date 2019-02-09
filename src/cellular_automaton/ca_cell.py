from cellular_automaton.ca_cell_state import CellState
from typing import Type


class Cell:
    def __init__(self, state_class: Type[CellState], coordinate):
        self._coordinate = coordinate
        self.state = state_class()
        self.neighbours = []

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def get_state(self):
        return self.state

    def get_coordinate(self):
        return self._coordinate

    def evolve_if_ready(self, rule, iteration):
        if self.state.is_active(iteration):
            new_state = rule(self.state.get_state_of_last_iteration(iteration), self.get_neighbour_states(iteration))
            self.set_new_state_and_activate(new_state, iteration)

    def get_neighbour_states(self, index):
        return [n.get_state_of_last_iteration(index) for n in self.neighbours]

    def set_new_state_and_activate(self, new_state: CellState, iteration):
        changed = self.state.set_state_of_iteration(new_state, iteration)
        if changed:
            self._set_active_for_next_iteration(iteration)

    def _set_active_for_next_iteration(self, iteration):
        self.state.set_active_for_next_iteration(iteration)
        for n in self.neighbours:
            n.set_active_for_next_iteration(iteration)
