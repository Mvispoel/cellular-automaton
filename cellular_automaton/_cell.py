from .cell_state import CellState
from typing import Type


class Cell:
    def __init__(self, state_class: Type[CellState]):
        self.state = state_class()
        self.neighbor_states = []

    def evolve_if_ready(self, rule, evolution_step):
        if self.state.is_active(evolution_step):
            new_state = rule(self.state.get_state_of_last_evolution_step(evolution_step),
                             [n.get_state_of_last_evolution_step(evolution_step) for n in self.neighbor_states])
            self.set_new_state_and_activate(new_state, evolution_step)

    def set_new_state_and_activate(self, new_state: CellState, evolution_step):
        changed = self.state.set_state_of_evolution_step(new_state, evolution_step)
        if changed:
            self.state.set_active_for_next_evolution_step(evolution_step)
            for n in self.neighbor_states:
                n.set_active_for_next_evolution_step(evolution_step)
