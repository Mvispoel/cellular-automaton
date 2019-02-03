#!/usr/bin/env python3

from cellular_automaton.ca_cell_state import CellState
from cellular_automaton.ca_rule import Rule

from cellular_automaton.cellular_automaton import CellularAutomaton, CellularAutomatonProcessor
from cellular_automaton.ca_factory import Factory


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
    ca_factory = Factory()
    cells = ca_factory.make_cellular_automaton(dimension=dimension, neighborhood=neighborhood, state_class=state_class)
    return CellularAutomaton(cells, dimension, rule)


if __name__ == "__main__":
    import random
    from multiprocessing import freeze_support
    from cellular_automaton.ca_neighborhood import MooreNeighborhood, EdgeRule
    from cellular_automaton.ca_display import PyGameFor2D

    freeze_support()

    random.seed(1000)
    # best is 400/400 with 0,2 ca speed and 0,09 redraw
    neighborhood = MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    ca = make_cellular_automaton(dimension=[100, 100], neighborhood=neighborhood, rule=TestRule(), state_class=MyState)
    ca_window = PyGameFor2D(window_size=[1000, 800], cellular_automaton=ca)
    ca_processor = CellularAutomatonProcessor(process_count=4, cellular_automaton=ca)
    ca_window.main_loop(cellular_automaton_processor=ca_processor,
                        ca_iterations_per_draw=5)
