import threading
import time

from cellular_automaton.ca_cell import CACell
from cellular_automaton.ca_grid import CAGrid


class CellularAutomaton:
    def __init__(self, threads=1):
        assert threads > 0
        self._thread_count = threads

    def evolve(self, grid, neighborhood, rule):
        range_ = int(len(grid) / self._thread_count)

        threads = []
        for t in range(self._thread_count):
            new_thread = EvolutionThread(grid, neighborhood, rule, [t * range_, t * range_ + range_])
            threads.append(new_thread)
            new_thread.start()

        new_grid_state = []
        for thread in threads:
            while not thread.is_finished():
                time.sleep(0.01)

            new_grid_state.extend(thread.get_new_cell_states())
            thread.join()

        return CAGrid(grid.get_dimensions(), new_grid_state)


class EvolutionThread(threading.Thread):
    def __init__(self, grid, neighborhood, rule, range_):
        super(EvolutionThread, self).__init__()
        self._grid = grid
        self._neighborhood = neighborhood
        self._rule = rule
        self._range = range_
        self._next_state = []
        self._finished = False

    def run(self):
        for cell_id in range(*self._range):
            neighbors = self._grid.get_all_neighbour_cells(cell_id, self._neighborhood)
            cell = self._grid[cell_id]
            self._next_state.append(CACell(self._rule.evolve_cell(cell, neighbors)))
        self._finished = True

    def get_new_cell_states(self):
        return self._next_state

    def is_finished(self):
        return self._finished
