import multiprocessing

from cellular_automaton.ca_rule import Rule
from cellular_automaton.ca_cell import Cell
from ctypes import c_int


class CellularAutomaton:
    def __init__(self, cells, dimension, evolution_rule: Rule):
        self.cells = cells
        self.dimension = dimension
        self.evolution_rule = evolution_rule
        self.evolution_iteration_index = -1


class CellularAutomatonProcessor:
    def __init__(self, cellular_automaton):
        self._ca = cellular_automaton

    def evolve_x_times(self, x):
        for x in range(x):
            self.evolve()

    def evolve(self):
        self._ca.evolution_iteration_index += 1
        i = self._ca.evolution_iteration_index
        r = self._ca.evolution_rule.evolve_cell
        list(map(lambda c: Cell.evolve_if_ready((c.state, c.neighbours), r, i), tuple(self._ca.cells.items())))
        # print(sum(1 for c in self._ca.cells if c.state.is_set_for_redraw()))


class CellularAutomatonMultiProcessor(CellularAutomatonProcessor):
    def __init__(self, cellular_automaton, process_count: int = 2):
        if process_count < 1:
            raise ValueError

        super().__init__(cellular_automaton)

        self.evolve_range = range(len(self._ca.cells))
        self.evolution_iteration_index = multiprocessing.RawValue(c_int, -1)

        self.pool = multiprocessing.Pool(processes=process_count,
                                         initializer=_init_process,
                                         initargs=(tuple(self._ca.cells.values()),
                                                   self._ca.evolution_rule,
                                                   self.evolution_iteration_index))
        self._evolve_method = self.pool.map

        for cell in self._ca.cells.values():
            del cell.neighbours

    def evolve(self):
        self._ca.evolution_iteration_index += 1
        self.evolution_iteration_index.value = self._ca.evolution_iteration_index
        self.pool.map(_process_routine, self.evolve_range)


global_cells = None
global_rule = None
global_iteration = None


def _init_process(cells, rule, index):
    global global_rule, global_cells, global_iteration
    global_cells = cells
    global_rule = rule
    global_iteration = index


def _process_routine(i):
    Cell.evolve_if_ready(global_cells[i], global_rule.evolve_cell, global_iteration.value)

