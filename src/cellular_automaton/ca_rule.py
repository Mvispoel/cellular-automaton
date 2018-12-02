from cellular_automaton.ca_cell import Cell
from abc import abstractmethod


class Rule:
    def __init__(self):
        pass

    @abstractmethod
    def evolve_cell(self, cell: Cell, neighbours: list, iteration_index: int):
        """ Calculates and sets new state of 'cell'.
        :param cell:              The cell to calculate new state for.
        :param neighbours:        The neighbour cells of this cell.
        :param iteration_index:   The current iteration index, to choose the correct state.
        :return: True if state changed, False if not.
        A cells evolution will only be called if it or at least one of its neighbours has changed last iteration cycle.
        """
        return False
