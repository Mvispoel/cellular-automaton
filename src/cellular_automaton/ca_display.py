import pygame
import time
import operator

import cProfile
import pstats
from pympler import asizeof


from cellular_automaton.cellular_automaton import CellularAutomaton, CellularAutomatonProcessor


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

    def redraw_cellular_automaton(self):
        update_rects = list(self._cell_redraw_rectangles())
        pygame.display.update(update_rects)

    def _cell_redraw_rectangles(self):
        for cell in self._cellular_automaton.cells:
            if cell.state.is_set_for_redraw():
                cell_color = cell.state.get_state_draw_color(self._cellular_automaton.evolution_iteration_index)
                cell_pos = _calculate_cell_position(self._display_info.cell_size, cell)
                surface_pos = list(map(operator.add, cell_pos, self._display_info.grid_pos))
                yield self._display_info.screen.fill(cell_color, (surface_pos, self._display_info.cell_size))
                cell.state.was_redrawn()

    def _calculate_cell_display_size(self, grid_size):
        grid_dimension = self._cellular_automaton.dimension
        return list(map(operator.truediv, grid_size, grid_dimension))


class PyGameFor2D:
    def __init__(self, window_size: list, cellular_automaton: CellularAutomaton):
        self._window_size = window_size
        self._cellular_automaton = cellular_automaton
        pygame.init()
        pygame.display.set_caption("Cellular Automaton")
        self._screen = pygame.display.set_mode(self._window_size)
        self._font = pygame.font.SysFont("monospace", 15)

        self.ca_display = DisplayFor2D([0, 30, window_size[0], window_size[1] - 30], cellular_automaton, self._screen)

    def _print_process_duration(self, time_ca_end, time_ca_start, time_ds_end):
        self._screen.fill([0, 0, 0], ((0, 0), (self._window_size[0], 30)))
        self._write_text((10, 5), "CA: " + "{0:.4f}".format(time_ca_end - time_ca_start) + "s")
        self._write_text((310, 5), "Display: " + "{0:.4f}".format(time_ds_end - time_ca_end) + "s")

    def _write_text(self, pos, text, color=(0, 255, 0)):
        label = self._font.render(text, 1, color)
        update_rect = self._screen.blit(label, pos)
        pygame.display.update(update_rect)

    def main_loop(self, cellular_automaton_processor: CellularAutomatonProcessor, ca_iterations_per_draw):
        running = True
        cellular_automaton_processor.evolve()
        first = True

        while running:
            pygame.event.get()
            time_ca_start = time.time()
            if first:
                self._evolve_with_performance(cellular_automaton_processor)
                first = False
            else:
                cellular_automaton_processor.evolve_x_times(ca_iterations_per_draw)
            time_ca_end = time.time()
            self.ca_display.redraw_cellular_automaton()
            time_ds_end = time.time()
            self._print_process_duration(time_ca_end, time_ca_start, time_ds_end)

    def _evolve_with_performance(self, cap):
        size = asizeof.asizeof(self._cellular_automaton)
        time_ca_start = time.time()
        cProfile.runctx("cap.evolve_x_times(10)", None, locals(), "performance_test")
        time_ca_end = time.time()
        print("PERFORMANCE")
        p = pstats.Stats('performance_test')
        p.strip_dirs()
        # sort by cumulative time in a function
        p.sort_stats('cumulative').print_stats(10)
        # sort by time spent in a function
        p.sort_stats('time').print_stats(10)
        print("TOTAL TIME: " + "{0:.4f}".format(time_ca_end - time_ca_start) + "s")
        print("SIZE: " + "{0:.4f}".format(size / (1024 * 1024)) + "MB")


def _calculate_cell_position(cell_size, cell):
    return list(map(operator.mul, cell_size, cell.coordinate))
