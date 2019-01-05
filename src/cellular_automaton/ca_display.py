import pygame
import time
import operator

from cellular_automaton.cellular_automaton import CellularAutomaton, CellularAutomatonEvolver


class _DisplayInfo:
    def __init__(self, grid_size, grid_pos, cell_size, screen):
        self.grid_size = grid_size
        self.grid_pos = grid_pos
        self.cell_size = cell_size
        self.screen = screen


class DisplayFor2D:
    def __init__(self, grid_rect: list, cellular_automaton: CellularAutomaton, screen):
        self._cellular_automaton = cellular_automaton
        cell_size = self._calculate_cell_display_size(grid_rect[-2:])
        self._display_info = _DisplayInfo(grid_rect[-2:], grid_rect[:2], cell_size, screen)

    def set_cellular_automaton(self, cellular_automaton):
        self._cellular_automaton = cellular_automaton

    def _redraw_cellular_automaton(self):
        pygame.display.update(list(_cell_redraw_rectangles(self._cellular_automaton.grid.get_cells().values(),
                                                           self._cellular_automaton.evolution_iteration_index,
                                                           self._display_info)))

    def _calculate_cell_display_size(self, grid_size):
        grid_dimension = self._cellular_automaton.grid.get_dimension()
        return list(map(operator.truediv, grid_size, grid_dimension))


class PyGameFor2D:
    def __init__(self,
                 windows_size: list,
                 cellular_automaton: CellularAutomaton,
                 cellular_automaton_evolver: CellularAutomatonEvolver,
                 ca_iterations_per_draw):
        self._window_size = windows_size
        self._cellular_automaton = cellular_automaton
        self._cellular_automaton_evolver = cellular_automaton_evolver
        self._ca_steps_per_draw = ca_iterations_per_draw

        pygame.init()
        pygame.display.set_caption("Cellular Automaton")
        self._screen = pygame.display.set_mode(self._window_size)
        self._font = pygame.font.SysFont("monospace", 15)

        self.ca_display = DisplayFor2D([0, 30, windows_size[0], windows_size[1]-30], cellular_automaton, self._screen)

    def _print_process_duration(self, time_ca_end, time_ca_start, time_ds_end):
        self._screen.fill([0, 0, 0], ((0, 0), (self._window_size[0], 30)))
        self._write_text((10, 5), "CA: " + "{0:.4f}".format(time_ca_end - time_ca_start) + "s")
        self._write_text((310, 5), "Display: " + "{0:.4f}".format(time_ds_end - time_ca_end) + "s")

    def _write_text(self, pos, text, color=(0, 255, 0)):
        label = self._font.render(text, 1, color)
        update_rect = self._screen.blit(label, pos)
        pygame.display.update(update_rect)

    def main_loop(self):
        running = True

        while running:
            time_ca_start = time.time()
            self._cellular_automaton_evolver.evolve_x_times(self._cellular_automaton, self._ca_steps_per_draw)
            time_ca_end = time.time()
            self.ca_display._redraw_cellular_automaton()
            time_ds_end = time.time()
            self._print_process_duration(time_ca_end, time_ca_start, time_ds_end)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


def _cell_redraw_rectangles(cells, evolution_index, display_info):
    for cell in cells:
        if cell.is_set_for_redraw:
            cell_color = cell.state.get_state_draw_color(evolution_index)
            cell_pos = _calculate_cell_position(display_info.cell_size, cell)
            surface_pos = list(map(operator.add, cell_pos, display_info.grid_pos))
            yield display_info.screen.fill(cell_color, (surface_pos, display_info.cell_size))
            cell.is_set_for_redraw = False


def _calculate_cell_position(cell_size, cell):
    return list(map(operator.mul, cell_size, cell.coordinate))
