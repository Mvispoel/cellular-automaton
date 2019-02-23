#!/usr/bin/env python3

import random
from cellular_automaton import *


class TestRule(Rule):
    random_seed = random.seed(1000)

    def init_state(self, cell_coordinate):
        rand = random.randrange(0, 101, 1)
        init = max(.0, float(rand - 99))
        return (init,)

    def evolve_cell(self, last_cell_state, neighbors_last_states):
        return self._get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, -1))

    def get_state_draw_color(self, current_state):
        return [255 if current_state[0] else 0, 0, 0]


if __name__ == "__main__":
    neighborhood = MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    ca = CAFactory.make_single_process_cellular_automaton(dimension=[100, 100],
                                                          neighborhood=neighborhood,
                                                          rule=TestRule)
    ca_window = CAWindow(cellular_automaton=ca, evolution_steps_per_draw=1)
