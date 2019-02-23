import multiprocessing
from multiprocessing import freeze_support
from ctypes import c_int


class CellularAutomatonProcessor:
    def __init__(self, cellular_automaton):
        self._ca = cellular_automaton

    def evolve_x_times(self, x):
        for x in range(x):
            self.evolve()

    def evolve(self):
        self._ca.current_evolution_step += 1
        i = self._ca.current_evolution_step
        r = self._ca.evolution_rule.evolve_cell
        list(map(lambda c: c.evolve_if_ready(r, i), tuple(self._ca.cells.values())))

    def get_dimension(self):
        return self._ca.dimension

    def get_cells(self):
        return self._ca.cells

    def get_current_evolution_step(self):
        return self._ca.current_evolution_step

    def get_current_rule(self):
        return self._ca.evolution_rule


class CellularAutomatonMultiProcessor(CellularAutomatonProcessor):
    def __init__(self, cellular_automaton, process_count: int = 2):
        freeze_support()
        if process_count < 1:
            raise ValueError

        super().__init__(cellular_automaton)

        self.evolve_range = range(len(self._ca.cells))
        self._ca.current_evolution_step = multiprocessing.RawValue(c_int, self._ca.current_evolution_step)

        self.__init_processes_and_clean_cell_instances(process_count)

    def __init_processes_and_clean_cell_instances(self, process_count):
        self.pool = multiprocessing.Pool(processes=process_count,
                                         initializer=_init_process,
                                         initargs=(tuple(self._ca.cells.values()),
                                                   self._ca.evolution_rule,
                                                   self._ca.current_evolution_step))
        for cell in self._ca.cells.values():
            del cell.neighbor_states

    def evolve(self):
        self._ca.current_evolution_step += 1
        self.pool.map(_process_routine, self.evolve_range)

    def get_current_evolution_step(self):
        return self._ca.current_evolution_step.value


global_cells = None
global_rule = None
global_evolution_step = None


def _init_process(cells, rule, index):
    global global_rule, global_cells, global_evolution_step
    global_cells = cells
    global_rule = rule
    global_evolution_step = index


def _process_routine(i):
    global_cells[i].evolve_if_ready(global_rule.evolve_cell, global_evolution_step.value)
