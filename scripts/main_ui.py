#!/usr/bin/env python3

import random
from cellular_automaton.ca_rule import Rule
from cellular_automaton.ca_cell_state import CellState, SynchronousCellState


class TestRule(Rule):
    @staticmethod
    def evolve_cell(last_cell_state, neighbors_last_states):
        try:
            return neighbors_last_states[0]
        except IndexError:
            return last_cell_state


# class MyState(SynchronousCellState):
class MyState(CellState):
    random_seed = random.seed(1000)

    def __init__(self):
        rand = random.randrange(0, 101, 1)
        init = max(.0, float(rand - 99))
        super().__init__((init,), draw_first_state=init > 0)

    def get_state_draw_color(self, evolution_step):
        state = self.get_state_of_evolution_step(evolution_step)[0]
        return [255 if state else 0, 0, 0]


if __name__ == "__main__":
    from cellular_automaton import *
    # best single is 400/400 with 0,2 ca speed and 0,09 redraw / multi is 300/300 with 0.083
    neighborhood = MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    ca = CAFactory.make_cellular_automaton(dimension=[100, 100],
                                           neighborhood=neighborhood,
                                           rule=TestRule(),
                                           state_class=MyState)
    # ca_processor = CellularAutomatonMultiProcessor(cellular_automaton=ca, process_count=4)
    ca_processor = CellularAutomatonProcessor(cellular_automaton=ca)

    ca_window = PyGameFor2D(window_size=[1000, 800], cellular_automaton=ca)
    ca_window.main_loop(cellular_automaton_processor=ca_processor, evolution_steps_per_draw=1)
