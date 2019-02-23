"""
Copyright 2019 Richard Feistenauer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import cellular_automaton.cellular_automaton.cell_state as cs


class Cell:
    def __init__(self, state_class: cs.CellState, neighbors):
        self._state = state_class
        self._neighbor_states = neighbors

    def is_set_for_redraw(self):
        return self._state.is_set_for_redraw()

    def was_redrawn(self):
        self._state.was_redrawn()

    def get_current_state(self, evolution_step):
        return self._state.get_state_of_evolution_step(evolution_step)

    def evolve_if_ready(self, rule, evolution_step):
        if self._state.is_active(evolution_step):
            new_state = rule(list(self._state.get_state_of_last_evolution_step(evolution_step)),
                             [list(n.get_state_of_last_evolution_step(evolution_step)) for n in self._neighbor_states])
            self.set_new_state_and_activate(new_state, evolution_step)

    def set_new_state_and_activate(self, new_state: cs.CellState, evolution_step):
        changed = self._state.set_state_of_evolution_step(new_state, evolution_step)
        if changed:
            self._state.set_active_for_next_evolution_step(evolution_step)
            for n in self._neighbor_states:
                n.set_active_for_next_evolution_step(evolution_step)
