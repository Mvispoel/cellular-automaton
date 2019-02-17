from enum import Enum
from operator import add
from itertools import product


class EdgeRule(Enum):
    IGNORE_EDGE_CELLS = 0
    IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS = 1
    FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS = 2


class Neighborhood:
    def __init__(self, neighbors_relative, edge_rule: EdgeRule):
        """ Defines a neighborhood of a cell.
        :param neighbors_relative: List of relative coordinates for cell neighbors.
        :param edge_rule: EdgeRule to define, how cells on the edge of the grid will be handled.
        """
        self._rel_neighbors = neighbors_relative
        self.__edge_rule = edge_rule
        self.__grid_dimensions = []

    def calculate_cell_neighbor_coordinates(self, cell_coordinate, grid_dimensions):
        """ Get a list of absolute coordinates for the cell neighbors.
            The EdgeRule can reduce the returned neighbor count.
        :param cell_coordinate:  The coordinate of the cell.
        :param grid_dimensions:  The dimensions of the grid, to apply the edge the rule.
        :return: list of absolute coordinates for the cells neighbors.
        """
        self.__grid_dimensions = grid_dimensions
        return list(self.__neighbors_generator(cell_coordinate))

    def __neighbors_generator(self, cell_coordinate):
        if not self.__does_ignore_edge_cell_rule_apply(cell_coordinate):
            for rel_n in self._rel_neighbors:
                yield from self.__calculate_abs_neighbor_and_decide_validity(cell_coordinate, rel_n)

    def __calculate_abs_neighbor_and_decide_validity(self, cell_coordinate, rel_n):
        n = list(map(add, rel_n, cell_coordinate))
        n_folded = self.__apply_edge_overflow(n)
        if n == n_folded or self.__edge_rule == EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS:
            yield n_folded

    def __does_ignore_edge_cell_rule_apply(self, coordinate):
        return self.__edge_rule == EdgeRule.IGNORE_EDGE_CELLS and self.__is_coordinate_on_an_edge(coordinate)

    def __is_coordinate_on_an_edge(self, coordinate):
        return all(0 == ci or ci == di-1 for ci, di in zip(coordinate, self.__grid_dimensions))

    def __apply_edge_overflow(self, n):
        return list(map(lambda ni, di: (ni + di) % di, n, self.__grid_dimensions))


class MooreNeighborhood(Neighborhood):
    def __init__(self, edge_rule: EdgeRule = EdgeRule.IGNORE_EDGE_CELLS, range_=1, dimension=2):
        super().__init__(tuple(_rel_neighbor_generator(dimension, range_, lambda rel_n: True)),
                         edge_rule)


class VonNeumannNeighborhood(Neighborhood):
    def __init__(self, edge_rule: EdgeRule = EdgeRule.IGNORE_EDGE_CELLS, range_=1, dimension=2):
        self.range_ = range_
        super().__init__(tuple(_rel_neighbor_generator(dimension, range_, self.neighbor_rule)),
                         edge_rule)

    def neighbor_rule(self, rel_n):
        cross_sum = 0
        for ci in rel_n:
            cross_sum += abs(ci)
        return cross_sum <= self.range_


def _rel_neighbor_generator(dimension, range_, rule):
    for c in product(range(-range_, range_ + 1), repeat=dimension):
        if rule(c) and c != (0, ) * dimension:
            yield tuple(reversed(c))
