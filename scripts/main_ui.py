#!/usr/bin/env python3

from cellular_automaton.ca_cell_state import CellState
from cellular_automaton.ca_rule import Rule


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


if __name__ == "__main__":
    import random
    from multiprocessing import freeze_support

    from cellular_automaton.cellular_automaton import CellularAutomaton, CellularAutomatonProcessor
    from cellular_automaton.ca_neighborhood import MooreNeighborhood, EdgeRule
    from cellular_automaton.ca_display import PyGameFor2D
    from cellular_automaton.ca_grid import Grid
    freeze_support()
    random.seed(1000)
    rule = TestRule()
    grid = Grid(dimension=[200, 200],  # best is 400/400 with 0,2 ca speed and 0,09 redraw
                neighborhood=MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS),
                state_class=MyState)
    ca = CellularAutomaton(grid, rule)
    ca_window = PyGameFor2D(window_size=[1000, 800], cellular_automaton=ca)
    ca_processor = CellularAutomatonProcessor(process_count=2, cellular_automaton=ca)
    ca_window.main_loop(cellular_automaton_processor=ca_processor,
                        ca_iterations_per_draw=5)
