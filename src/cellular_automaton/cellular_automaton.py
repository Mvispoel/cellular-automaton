from cellular_automaton.ca_grid import Grid
from cellular_automaton.ca_rule import Rule
from cellular_automaton.ca_neighborhood import Neighborhood


class CellularAutomaton:
    def __init__(self, dimension: list, neighborhood: Neighborhood, evolution_rule: Rule=None):
        self.grid = Grid(dimension, neighborhood)
        self.evolution_rule = evolution_rule
        self.iteration = 0
        self.test_number = 0

    def set_rule(self, rule: Rule):
        """ Set new evolution rule.
        :param rule:
        :return:
        """
        self.evolution_rule = rule

    def get_iteration_index(self):
        """ Get the count of evolution cycles done.
        :return: Evolution steps done.
        """
        return self.iteration

    def evolve_x_times(self, evolutions: int):
        """ Evolve all cells for x time steps.
        :param evolutions: the count of evolutions done.
        :return: True if all cells are inactive
        """
        for evo in range(evolutions):
            finished = self.evolve()
            if finished:
                return True
        return False

    def evolve(self):
        """ Evolves all active cells for one time step.
        :return: True if all cells are inactive.
        """
        if self._is_evolution_finished():
            return True
        else:
            self.iteration += 1
            self._evolve_all_active_cells()
            return False

    def _evolve_all_active_cells(self):
        active_cells = self.grid.get_active_cells()
        self.grid.clear_active_cells()
        self._evolve_cells(active_cells.values())

    def _is_evolution_finished(self):
        return len(self.grid.get_active_cell_names()) == 0

    def _evolve_cells(self, cells: list):
        for cell in cells:
            active = self.evolution_rule.evolve_cell(cell, self.iteration)

            if active:
                self.grid.set_cells_active([cell] + cell.neighbours)
