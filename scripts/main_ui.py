#!/usr/bin/env python3

import random

from cellular_automaton.cellular_automaton import CellularAutomaton, CellularAutomatonProcessor
from cellular_automaton.ca_rule import Rule
from cellular_automaton.ca_neighborhood import MooreNeighborhood, EdgeRule
from cellular_automaton.ca_display import PyGameFor2D
from cellular_automaton.ca_cell_state import CellState
from cellular_automaton.ca_grid import Grid


class TestRule(Rule):
    def evolve_cell(self, cell, iteration_index):
        if cell.state is None:
            return self._init_state(cell)
        else:
            return self._evolve_state(cell, iteration_index)

    @staticmethod
    def _evolve_state(cell, iteration_index):
        try:
            left_neighbour_state = cell.neighbours[0].state.get_status_of_iteration(iteration_index - 1)
            active = cell.state.set_status_of_iteration(left_neighbour_state, iteration_index)
            if active:
                cell.is_set_for_redraw = True
            return active
        except IndexError:
            return False

    @staticmethod
    def _init_state(cell):
        rand = random.randrange(0, 101, 1)
        if rand <= 99:
            cell.state = MyStatus(0)
            return False
        else:
            cell.state = MyStatus(1)
            cell.is_set_for_redraw = True
            return True


class MyStatus(CellState):
    def __init__(self, initial_state):
        super().__init__([initial_state])

    def get_state_draw_color(self, iteration):
        red = 0
        if self._state_slots[iteration % 2][0]:
            red = 255
        return [red, 0, 0]


if __name__ == "__main__":
    random.seed(1000)
    rule = TestRule()
    grid = Grid(dimension=[400, 400],
                neighborhood=MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS))
    ca = CellularAutomaton(grid, rule)
    ca_window = PyGameFor2D(window_size=[1000, 800], cellular_automaton=ca)
    ca_processor = CellularAutomatonProcessor(process_count=8)
    ca_window.main_loop(cellular_automaton_processor=ca_processor,
                        ca_iterations_per_draw=5)
