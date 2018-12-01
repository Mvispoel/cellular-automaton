import abc


class CARule(abc.ABC):
    @abc.abstractmethod
    def evolve_cell(self, cell, neighbors):
        """
        Evolves a cell and returns its new state as list of states.
        :param cell:        The cell to evolve.
        :param neighbors:   A list of its neighbors.
        :return:    The new state list.
        """
        pass
