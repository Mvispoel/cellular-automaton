from cellular_automaton.ca_cell_state import CellState
from typing import Type


class Cell:
    def __init__(self, state_class: Type[CellState], coordinate):
        self.coordinate = coordinate
        self.state = state_class()
        self.neighbours = []

    @staticmethod
    def evolve_if_ready(cell, rule, iteration):
        if cell[0].is_active(iteration):
            new_state = rule(cell[0].get_state_of_last_iteration(iteration),
                             [n.get_state_of_last_iteration(iteration) for n in cell[1]])
            Cell.set_new_state_and_activate(cell, new_state, iteration)

    @staticmethod
    def set_new_state_and_activate(cell, new_state: CellState, iteration):
        changed = cell[0].set_state_of_iteration(new_state, iteration)
        if changed:
            cell[0].set_active_for_next_iteration(iteration)
            for n in cell[1]:
                n.set_active_for_next_iteration(iteration)
