import multiprocessing
import time

from cellular_automaton.ca_grid import Grid
from cellular_automaton.ca_rule import Rule
from cellular_automaton.ca_neighborhood import Neighborhood


class CellularAutomaton:
    def __init__(self, dimension: list, neighborhood: Neighborhood, rule_: Rule=None, thread_count: int=4):
        self.grid = Grid(dimension, neighborhood)
        self.rule = rule_
        self._thread_count = thread_count
        self.iteration = 0
        self.test_number = 0

    def set_rule(self, rule: Rule):
        self.rule = rule

    def set_thread_count(self, thread_count: int):
        self._thread_count = thread_count

    def get_iteration_index(self):
        return self.iteration

    def evolve(self):
        """ Evolves all active cells for one time step.
        :return: True if all cells are inactive.
        """
        if self._all_cells_are_inactive():
            return True
        else:
            self.iteration += 1
            self._start_multi_process_cell_evolution()
            return False

    def _start_multi_process_cell_evolution(self):
        """ Evolves the cells in separate threads """
        lists_of_cell_names = self._create_list_of_cell_names_lists_for_all_threads()
        self.grid.clear_active_cells()
        jobs = self._start_treads_to_evolve_grid(lists_of_cell_names)
        self._wait_for_all_threads_to_finish(jobs)
        print(self.test_number)

    def _all_cells_are_inactive(self):
        return len(self.grid.get_names_of_active_cells()) == 0

    def _create_list_of_cell_names_lists_for_all_threads(self):
        active_cells = self.grid.get_names_of_active_cells()
        cell_count_per_thread = int(len(active_cells) / self._thread_count)
        return self._divide_list_in_parts_of_size(active_cells, cell_count_per_thread)

    @staticmethod
    def _divide_list_in_parts_of_size(active_cells: list, cell_count_per_thread: int):
        return [active_cells[i:i + cell_count_per_thread]
                for i in range(0, len(active_cells), cell_count_per_thread)]

    def _start_treads_to_evolve_grid(self, lists_of_cell_names):
        jobs = []
        for t in range(self._thread_count):
            process = multiprocessing.Process(target=_evolve_cells, args=(self, lists_of_cell_names[t]))
            jobs.append(process)
            process.start()
        return jobs

    @staticmethod
    def _wait_for_all_threads_to_finish(jobs):
        for process in jobs:
            process.join()


def _evolve_cells(cellular_automaton, cell_names: list):
    time.sleep(2)
    cellular_automaton.test_number += 1
    print(cellular_automaton.grid)
    for cell_name in cell_names:
        cell_info = cellular_automaton.grid.get_cell_and_neighbors(cell_name)
        active = cellular_automaton.rule.evolve_cell(cell_info[0], cell_info[1], cellular_automaton.iteration)

        if active:
            cellular_automaton.grid.set_cell_and_neighbours_active(cell_info)
