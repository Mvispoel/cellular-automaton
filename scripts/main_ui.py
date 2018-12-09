#!/usr/bin/env python3

import pygame
import random
import time

from cellular_automaton.cellular_automaton import CellularAutomaton
from cellular_automaton.ca_rule import Rule
from cellular_automaton.ca_neighborhood import MooreNeighborhood, EdgeRule
from cellular_automaton.ca_display import PyGameFor2D
from cellular_automaton.ca_cell_state import CellState


class WorldGeneratorWindow:
    def __init__(self, windows_size: list, cellular_automaton: CellularAutomaton):
        self.window_size = windows_size
        self.grid_size = self.window_size.copy()
        self.grid_size[1] -= 20

        pygame.init()
        pygame.display.set_caption("World Generator")
        self.screen = pygame.display.set_mode(self.window_size)

        self._cellular_automaton = cellular_automaton
        self.font = pygame.font.SysFont("monospace", 15)

    def set_cellular_automaton(self, cellular_automaton):
        self._cellular_automaton = cellular_automaton

    def _display_cellular_automaton(self):
        grid_dimension = self._cellular_automaton.grid.get_dimension()

        cell_size = [x / y for x, y in zip(self.grid_size, grid_dimension)]

        surfaces_to_update = []
        for cell in self._cellular_automaton.grid.get_cells().values():
            if not cell.is_set_for_redrawing():
                continue
            cell_coordinate = cell.coordinate
            status = cell.get_status_for_iteration(self._cellular_automaton.get_iteration_index())
            if status is None:
                status = [0]
            red = 0
            if status[0] >= 10:
                red = 255
            cell_color = [red, 0, 0]
            surface_pos = [x * y for x, y in zip(cell_size, cell_coordinate)]
            surface_pos[1] += 20
            surfaces_to_update.append(self.screen.fill(cell_color, (surface_pos, cell_size)))
            cell.release_from_redraw()
        pygame.display.update(surfaces_to_update)

    def main_loop(self):
        running = True

        while running:
            time_ca_start = time.time()
            self._cellular_automaton.evolve_x_times(10)
            time_ca_end = time.time()
            self._display_cellular_automaton()
            time_ds_end = time.time()
            self._print_process_duration(time_ca_end, time_ca_start, time_ds_end)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def _print_process_duration(self, time_ca_end, time_ca_start, time_ds_end):
        self.screen.fill([0, 0, 0], ((0, 0), (self.window_size[0], 30)))
        self._write_text((10, 5), "CA: " + "{0:.4f}".format(time_ca_end - time_ca_start) + "s")
        self._write_text((310, 5), "Display: " + "{0:.4f}".format(time_ds_end - time_ca_end) + "s")

    def _write_text(self, pos, text, color=(0, 255, 0)):
        label = self.font.render(text, 1, color)
        update_rect = self.screen.blit(label, pos)
        pygame.display.update(update_rect)


class TestRule(Rule):
    def evolve_cell(self, cell, neighbors, iteration_index):
        active = False
        last_iteration = iteration_index - 1
        if cell.state is None:
            rand = random.randrange(0, 101, 1)
            if rand <= 99:
                cell.state = MyStatus(0)
            else:
                cell.state = MyStatus(1)
                cell.set_for_redraw()
                active = True
        elif len(neighbors) == 8:
            left_neighbour_status = neighbors[3].state.get_status_of_iteration(last_iteration)
            active = cell.state.set_status_of_iteration(left_neighbour_status, iteration_index)
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
    rule = TestRule()
    ca = CellularAutomaton([400, 400], MooreNeighborhood(EdgeRule.IGNORE_EDGE_CELLS), rule)
    ca_window = PyGameFor2D([1000, 730], ca)
    ca_window.main_loop()
