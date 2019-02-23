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

import abc
import cellular_automaton.cellular_automaton.neighborhood as neighbour


class Rule:
    def __init__(self, neighborhood_: neighbour.Neighborhood):
        self._neighborhood = neighborhood_

    def _get_neighbor_by_relative_coordinate(self, neighbours, rel_coordinate):
        return neighbours[self._neighborhood.get_neighbor_id_from_rel(rel_coordinate)]

    @abc.abstractmethod
    def evolve_cell(self, last_cell_state, neighbors_last_states):
        """ Calculates and sets new state of 'cell'.
        :param last_cell_state:   The cells current state to calculate new state for.
        :param neighbors_last_states:  The cells neighbors current states.
        :return: New state.
        A cells evolution will only be called if it or at least one of its neighbors has changed last evolution_step cycle.
        """
        return last_cell_state

    @abc.abstractmethod
    def init_state(self, cell_coordinate):
        """ Set the initial state for the cell with the given coordinate.
        :param cell_coordinate: Cells coordinate.
        :return: Iterable that represents the state
        """
        return [0]

    @abc.abstractmethod
    def get_state_draw_color(self, current_state):
        return [0, 0, 0]
