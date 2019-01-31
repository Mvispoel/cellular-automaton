import multiprocessing

from cellular_automaton.ca_grid import Grid
from cellular_automaton.ca_rule import Rule


class CellularAutomaton:
    def __init__(self, grid: Grid, evolution_rule: Rule):
        self.grid = grid
        self.evolution_rule = evolution_rule
        self.evolution_iteration_index = 0


class CellularAutomatonProcessor:
    def __init__(self, cellular_automaton, process_count: int = 1):
        self.active = multiprocessing.Value('i', 1)
        cells = list(cellular_automaton.grid.get_cells().values())
        chunk_size = int(len(cells) / process_count)
        self._processes = [multiprocessing.Process(target=_process_routine,
                                                   name=str(i),
                                                   args=(cells[i*chunk_size:i*chunk_size + chunk_size],
                                                         cellular_automaton.evolution_rule,
                                                         self.active))
                           for i in range(process_count)]
        for p in self._processes:
            p.start()
        self.__cellular_automaton = None

    def stop(self):
        self.active.value = 0
        for p in self._processes:
            p.join()


def _process_routine(cells, rule, active):
    while active.value == 1:
        for cell in cells:
            cell.evolve_if_ready(rule)

