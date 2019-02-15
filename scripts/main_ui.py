#!/usr/bin/env python3

import random
from multiprocessing import freeze_support
from cellular_automaton import *


class TestRule(Rule):
    @staticmethod
    def evolve_cell(last_cell_state, neighbours_last_states):
        try:
            return neighbours_last_states[0]
        except IndexError:
            return last_cell_state


class MyState(SynchronousCellState):
    def __init__(self):
        rand = random.randrange(0, 101, 1)
        init = max(.0, float(rand - 99))
        super().__init__((init,), draw_first_state=init > 0)

    def get_state_draw_color(self, iteration):
        state1 = self.get_state_of_iteration(iteration)[0]
        return [255 if state1 else 0, 0, 0]


def make_cellular_automaton(dimension, neighborhood, rule, state_class):
    cells = CAFactory.make_cellular_automaton(dimension=dimension, neighborhood=neighborhood, state_class=state_class)
    return CellularAutomaton(cells, dimension, rule)


if __name__ == "__main__":
    freeze_support()

    random.seed(1000)
    # best single is 400/400 with 0,2 ca speed and 0,09 redraw / multi is 300/300 with 0.083
    neighborhood = MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    ca = make_cellular_automaton(dimension=[100, 100], neighborhood=neighborhood, rule=TestRule(), state_class=MyState)
    ca_processor = CellularAutomatonMultiProcessor(cellular_automaton=ca, process_count=4)

    ca_window = PyGameFor2D(window_size=[1000, 800], cellular_automaton=ca)
    ca_window.main_loop(cellular_automaton_processor=ca_processor, ca_iterations_per_draw=1)
