import pygame
import time
import operator

from cellular_automaton.cellular_automaton import CellularAutomaton


class DisplayFor2D:
    def __init__(self, grid_rect: list, cellular_automaton: CellularAutomaton, screen):
        self.grid_size = grid_rect[-2:]
        self.grid_pos = grid_rect[:2]
        self._cellular_automaton = cellular_automaton
        self.screen = screen

        self.cell_size = self._calculate_cell_display_size()

        self._surfaces_to_update = []

    def set_cellular_automaton(self, cellular_automaton):
        self._cellular_automaton = cellular_automaton

    def _redraw_cellular_automaton(self):
        for cell in self._cellular_automaton.grid.get_cells().values():
            self._redraw_cell(cell)
        pygame.display.update(self._surfaces_to_update)
        self._surfaces_to_update = []

    def _redraw_cell(self, cell):
        if cell.is_set_for_redrawing():
            cell_color = cell.state.get_state_draw_color(self._cellular_automaton.get_iteration_index())
            surface_pos = self._calculate_cell_position(cell)
            surface_pos = list(map(operator.add, surface_pos, self.grid_pos))
            self._surfaces_to_update.append(self.screen.fill(cell_color, (surface_pos, self.cell_size)))
            cell.release_from_redraw()

    def _calculate_cell_position(self, cell):
        return list(map(operator.mul, self.cell_size, cell.coordinate))

    def _calculate_cell_display_size(self):
        grid_dimension = self._cellular_automaton.grid.get_dimension()
        return list(map(operator.truediv, self.grid_size, grid_dimension))


class PyGameFor2D:
    def __init__(self, windows_size: list, cellular_automaton: CellularAutomaton):
        self.window_size = windows_size
        self._cellular_automaton = cellular_automaton

        pygame.init()
        pygame.display.set_caption("Cellular Automaton")
        self.screen = pygame.display.set_mode(self.window_size)
        self.font = pygame.font.SysFont("monospace", 15)

        self.ca_display = DisplayFor2D([0, 30, windows_size[0], windows_size[1]-30], cellular_automaton, self.screen)

    def _print_process_duration(self, time_ca_end, time_ca_start, time_ds_end):
        self.screen.fill([0, 0, 0], ((0, 0), (self.window_size[0], 30)))
        self._write_text((10, 5), "CA: " + "{0:.4f}".format(time_ca_end - time_ca_start) + "s")
        self._write_text((310, 5), "Display: " + "{0:.4f}".format(time_ds_end - time_ca_end) + "s")

    def _write_text(self, pos, text, color=(0, 255, 0)):
        label = self.font.render(text, 1, color)
        update_rect = self.screen.blit(label, pos)
        pygame.display.update(update_rect)

    def main_loop(self):
        running = True

        while running:
            time_ca_start = time.time()
            self._cellular_automaton.evolve_x_times(5)
            time_ca_end = time.time()
            self.ca_display._redraw_cellular_automaton()
            time_ds_end = time.time()
            self._print_process_duration(time_ca_end, time_ca_start, time_ds_end)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

