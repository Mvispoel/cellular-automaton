import threading
import time

from cellular_automaton.ca_grid import Grid
from cellular_automaton.ca_rule import Rule
from cellular_automaton.ca_neighborhood import Neighborhood


class CellularAutomaton:
    def __init__(self, dimension: list, neighborhood: Neighborhood, rule_: Rule=None, thread_count: int=4):
        self.grid = Grid(dimension, neighborhood)
        self._rule = rule_
        self._thread_count = thread_count
        self._iteration = 0

    def set_rule(self, rule: Rule):
        self._rule = rule

    def set_thread_count(self, thread_count: int):
        self._thread_count = thread_count

    def get_iteration_index(self):
        return self._iteration

    def evolve(self):
        if self._all_cells_are_inactive():
            return True
        else:
            self._iteration += 1
            self._delegate_evolve_to_threads()
            return False

    def _delegate_evolve_to_threads(self):
        cell_lists_for_threats = self.create_cell_lists_for_threads()
        self.grid.clear_active_cells()
        threads = self._start_treads_to_evolve_grid(cell_lists_for_threats)
        self._wait_for_all_threads_to_finish(threads)

    def _all_cells_are_inactive(self):
        return len(self.grid.get_names_of_active_cells()) == 0

    def create_cell_lists_for_threads(self):
        active_cells = self.grid.get_names_of_active_cells()
        cell_count_per_thread = int(len(active_cells) / self._thread_count)
        return self.divide_active_cells(cell_count_per_thread, active_cells)

    @staticmethod
    def divide_active_cells(cell_count_per_thread, active_cells):
        return [active_cells[i:i + cell_count_per_thread]
                for i in range(0, len(active_cells), cell_count_per_thread)]

    def _start_treads_to_evolve_grid(self, cell_lists_for_threats):
        threads = []
        for t in range(self._thread_count):
            new_thread = _EvolutionThread(self.grid, self._rule, cell_lists_for_threats[t], self._iteration)
            threads.append(new_thread)
            new_thread.start()
        return threads

    @staticmethod
    def _wait_for_all_threads_to_finish(threads):
        for thread in threads:
            while not thread.is_finished():
                time.sleep(0.01)

            thread.join()


class _EvolutionThread(threading.Thread):
    def __init__(self, grid: Grid, rule: Rule, cell_list: list, iteration: int):
        super(_EvolutionThread, self).__init__()
        self._grid = grid
        self._rule = rule
        self._cell_list = cell_list
        self._next_state = []
        self._finished = False
        self._iteration = iteration

    def run(self):
        for cell in self._cell_list:
            cell_info = self._grid.get_cell_and_neighbors(cell)
            active = self._rule.evolve_cell(cell_info[0], cell_info[1], self._iteration)

            if active:
                self._grid.set_cell_and_neighbours_active(cell_info)
        self._finished = True

    def get_new_cell_states(self):
        return self._next_state

    def is_finished(self):
        return self._finished
