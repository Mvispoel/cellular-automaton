import threading
import time

from cellular_automaton.ca_grid import Grid
from cellular_automaton.ca_rule import Rule


class CellularAutomaton:
    def __init__(self, dimension: list, rule_: Rule=None, thread_count: int=4):
        self.grid = Grid(dimension)
        self._rule = rule_
        self._thread_count=thread_count

    def set_rule(self, rule: Rule):
        self._rule = rule

    def set_thread_count(self, thread_count: int):
        self._thread_count = thread_count

    def evolve(self):
        cell_lists_for_threats = self.create_cell_lists_for_threads()
        threads = self._start_treads_to_evolve_grid(cell_lists_for_threats)
        self._wait_for_all_threads_to_finish(threads)

    def create_cell_lists_for_threads(self):
        active_cells = self.grid.get_active_cells()
        cell_count_per_thread = int(len(active_cells) / self._thread_count)
        return self.divide_active_cells(cell_count_per_thread, active_cells)

    @staticmethod
    def divide_active_cells(cell_count_per_thread, active_cells):
        return [active_cells[i:i + cell_count_per_thread]
                for i in range(0, len(active_cells), cell_count_per_thread)]

    def _start_treads_to_evolve_grid(self, cell_lists_for_threats):
        threads = []
        for t in range(self._thread_count):
            new_thread = _EvolutionThread(self.grid, self._rule, cell_lists_for_threats[t])
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
    def __init__(self, grid: Grid, rule: Rule, cell_list: list):
        super(_EvolutionThread, self).__init__()
        self._grid = grid
        self._rule = rule
        self._cell_list = cell_list
        self._next_state = []
        self._finished = False

    def run(self):
        for cell in self._cell_list:
            self._rule.evolve_cell(*self._grid.get_cell_and_neighbors(cell))
        self._finished = True

    def get_new_cell_states(self):
        return self._next_state

    def is_finished(self):
        return self._finished
