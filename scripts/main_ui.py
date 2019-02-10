#!/usr/bin/env python3

import random
from multiprocessing import freeze_support
from cellular_automaton import *


class TestRule(Rule):
    @staticmethod
    def evolve_cell(last_cell_state, last_neighbour_states):
        try:
            return last_neighbour_states[0]
        except IndexError:
            print("damn neighbours")
            pass
        return False


class MyState(CellState):
    def __init__(self):
        rand = random.randrange(0, 101, 1)
        init = 0
        if rand > 99:
            init = 1

        super().__init__((float(init),), draw_first_state=False)

    def get_state_draw_color(self, iteration):
        red = 0
        if self.get_state_of_last_iteration(iteration)[0]:
            red = 255
        return [red, 0, 0]


def make_cellular_automaton(dimension, neighborhood, rule, state_class):
    cells = CAFactory.make_cellular_automaton(dimension=dimension, neighborhood=neighborhood, state_class=state_class)
    return CellularAutomaton(cells, dimension, rule)


if __name__ == "__main__":
    freeze_support()

    random.seed(1000)
    # best single is 400/400 with 0,2 ca speed and 0,09 redraw / multi is 300/300 with 0.083
    neighborhood = MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    ca = make_cellular_automaton(dimension=[400, 400], neighborhood=neighborhood, rule=TestRule(), state_class=MyState)
    ca_processor = CellularAutomatonProcessor(process_count=1, cellular_automaton=ca)

    ca_window = PyGameFor2D(window_size=[1000, 800], cellular_automaton=ca)
    ca_window.main_loop(cellular_automaton_processor=ca_processor, ca_iterations_per_draw=1)
