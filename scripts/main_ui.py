#!/usr/bin/env python3

import random

from cellular_automaton.cellular_automaton import CellularAutomaton
from cellular_automaton.ca_rule import Rule
from cellular_automaton.ca_neighborhood import MooreNeighborhood, EdgeRule
from cellular_automaton.ca_display import PyGameFor2D
from cellular_automaton.ca_cell_state import CellState


class TestRule(Rule):
    def evolve_cell(self, cell, neighbors, iteration_index):
        active = False
        if cell.state is None:
            rand = random.randrange(0, 101, 1)
            if rand <= 99:
                cell.state = MyStatus(0)
            else:
                cell.state = MyStatus(1)
                cell.set_for_redraw()
                active = True
        elif len(neighbors) == 8:
            left_neighbour_state = neighbors[3].state.get_status_of_iteration(iteration_index - 1)
            active = cell.state.set_status_of_iteration(left_neighbour_state, iteration_index)
            if active:
                cell.set_for_redraw()
        return active


class MyStatus(CellState):
    def __init__(self, initial_state):
        super().__init__(initial_state)

    def get_state_draw_color(self, iteration):
        red = 0
        if self._state[iteration % 2][0]:
            red = 255
        return [red, 0, 0]


if __name__ == "__main__":
    random.seed(1000)
    rule = TestRule()
    ca = CellularAutomaton([500, 500], MooreNeighborhood(EdgeRule.IGNORE_EDGE_CELLS), rule)
    ca_window = PyGameFor2D([1000, 730], ca)
    ca_window.main_loop()
