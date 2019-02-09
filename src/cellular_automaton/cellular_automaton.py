import multiprocessing

from cellular_automaton.ca_rule import Rule


class CellularAutomaton:
    def __init__(self, cells, dimension, evolution_rule: Rule):
        self.cells = cells
        self.dimension = dimension
        self.evolution_rule = evolution_rule
        self.evolution_iteration_index = multiprocessing.RawValue('i', -1)


class CellularAutomatonProcessor:
    def __init__(self, cellular_automaton, process_count: int = 1):
        self.ca = cellular_automaton
        cells = {i: self.ca.cells[i] for i in range(len(self.ca.cells))}
        self.evolve_range = range(len(self.ca.cells))
        self.pool = multiprocessing.Pool(processes=process_count,
                                         initializer=_init_process,
                                         initargs=(cells,
                                                   self.ca.evolution_rule,
                                                   self.ca.evolution_iteration_index))
        for cell in self.ca.cells:
            cell.set_neighbours(None)

    def evolve_x_times(self, x):
        for x in range(x):
            self.evolve()

    def evolve(self):
        self.ca.evolution_iteration_index.value += 1
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
    global_cells[i].evolve_if_ready(global_rule.evolve_cell, global_iteration.value)

