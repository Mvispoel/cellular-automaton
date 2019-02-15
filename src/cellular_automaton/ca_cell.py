from cellular_automaton.ca_cell_state import CellState
from typing import Type


class Cell:
    def __init__(self, state_class: Type[CellState]):
        self.state = state_class()
        self.neighbours = []

    @staticmethod
    def evolve_if_ready(cell, rule, iteration):
        if cell.state.is_active(iteration):
            new_state = rule(cell.state.get_state_of_last_iteration(iteration),
                             [n.get_state_of_last_iteration(iteration) for n in cell.neighbours])
            Cell.set_new_state_and_activate(cell, new_state, iteration)

    @staticmethod
    def set_new_state_and_activate(cell, new_state: CellState, iteration):
        changed = cell.state.set_state_of_iteration(new_state, iteration)
        if changed:
            cell.state.set_active_for_next_iteration(iteration)
            for n in cell.neighbours:
                n.set_active_for_next_iteration(iteration)
