#!/usr/bin/env python3

import random
from cellular_automaton import *


ALIVE = [1.0]
DEAD = [0]


class TestRule(Rule):
    random_seed = random.seed(13)

    def init_state(self, cell_coordinate):
        rand = random.randrange(0, 16, 1)
        init = max(.0, float(rand - 14))
        return [init]

    def evolve_cell(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state
        alive_neighbours = self.__count_alive_neighbours(neighbors_last_states)
        if last_cell_state == DEAD and alive_neighbours == 3:
            new_cell_state = ALIVE
        if last_cell_state == ALIVE and alive_neighbours < 2:
            new_cell_state = DEAD
        if last_cell_state == ALIVE and 1 < alive_neighbours < 4:
            new_cell_state = ALIVE
        if last_cell_state == ALIVE and alive_neighbours > 3:
            new_cell_state = DEAD
        return new_cell_state

    @staticmethod
    def __count_alive_neighbours(neighbours):
        an = []
        for n in neighbours:
            if n == ALIVE:
                an.append(1)
        return len(an)

    def get_state_draw_color(self, current_state):
        return [255 if current_state[0] else 0, 0, 0]


if __name__ == "__main__":
    neighborhood = MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    ca = CAFactory.make_multi_process_cellular_automaton(dimension=[100, 100],
                                                         neighborhood=neighborhood,
                                                         rule=TestRule,
                                                         processes=4)
    ca_window = CAWindow(cellular_automaton=ca, evolution_steps_per_draw=1)
