from cellular_automaton.ca_grid import Grid
from cellular_automaton.ca_rule import Rule


class CellularAutomaton:
    def __init__(self, grid: Grid, evolution_rule: Rule):
        self.grid = grid
        self.evolution_rule = evolution_rule
        self.evolution_iteration_index = 0


class CellularAutomatonEvolver:
    def __init__(self, process_count: int = 1):
        self.__processes = process_count
        self.__cellular_automaton = None

    def evolve_x_times(self, cellular_automaton: CellularAutomaton, evolution_steps: int):
        """ Evolve all cells for x time steps.
        :param evolution_steps: the count of evolutions done.
        :return: True if all cells are inactive
        """
        for evo in range(evolution_steps):
            finished = self.evolve(cellular_automaton)
            if finished:
                return True
        return False

    def evolve(self, cellular_automaton: CellularAutomaton):
        """ Evolves all active cells for one time step.
        :return: True if all cells are inactive.
        """
        self.__cellular_automaton = cellular_automaton
        if self._is_evolution_finished():
            return True
        else:
            cellular_automaton.evolution_iteration_index += 1
            self._evolve_all_active_cells()
            return False

    def _is_evolution_finished(self):
        return len(self.__cellular_automaton.grid.get_active_cell_names()) == 0

    def _evolve_all_active_cells(self):
        active_cells = self.__cellular_automaton.grid.get_active_cells()
        self.__cellular_automaton.grid.clear_active_cells()
        self._evolve_cells(active_cells.values())

    def _evolve_cells(self, cells: list):
        cellular_automaton = self.__cellular_automaton
        for cell in cells:
            active = cellular_automaton.evolution_rule.evolve_cell(cell, cellular_automaton.evolution_iteration_index)

            if active:
                cellular_automaton.grid.set_cells_active([cell] + cell.neighbours)
