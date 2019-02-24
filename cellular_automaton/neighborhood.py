"""
Copyright 2019 Richard Feistenauer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import enum
import operator
import itertools


class EdgeRule(enum.Enum):
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

    def get_id_of_neighbor_from_relative_coordinate(self, rel_coordinate):
        return self._rel_neighbors.index(rel_coordinate)

    def __neighbors_generator(self, cell_coordinate):
        if not self.__does_ignore_edge_cell_rule_apply(cell_coordinate):
            for rel_n in self._rel_neighbors:
                yield from self.__calculate_abs_neighbor_and_decide_validity(cell_coordinate, rel_n)

    def __calculate_abs_neighbor_and_decide_validity(self, cell_coordinate, rel_n):
        n = list(map(operator.add, rel_n, cell_coordinate))
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
    """ Defines a Moore neighborhood:
        Moore defined a neighborhood with a radius applied on a the non euclidean distance to other cells in the grid.
        Example:
            Moor neighborhood in 2 dimensions with radius 1 and 2
            C = cell of interest
            N = neighbour of cell
            X = no neighbour of cell

                  Radius 1                     Radius 2
               X  X  X  X  X                N  N  N  N  N
               X  N  N  N  X                N  N  N  N  N
               X  N  C  N  X                N  N  C  N  N
               X  N  N  N  X                N  N  N  N  N
               X  X  X  X  X                N  N  N  N  N
    """

    def __init__(self, edge_rule: EdgeRule = EdgeRule.IGNORE_EDGE_CELLS, range_=1, dimension=2):
        super().__init__(tuple(_rel_neighbor_generator(dimension, range_, lambda rel_n: True)),
                         edge_rule)


class VonNeumannNeighborhood(Neighborhood):
    """ Defines a Von Neumann neighborhood:
        Von Neumann defined a neighborhood with a radius applied to Manhatten distance
        (steps between cells without diagonal movement).
        Example:
            Von Neumann neighborhood in 2 dimensions with radius 1 and 2
            C = cell of interest
            N = neighbour of cell
            X = no neighbour of cell

                  Radius 1                     Radius 2
               X  X  X  X  X                X  X  N  X  X
               X  X  N  X  X                X  N  N  N  X
               X  N  C  N  X                N  N  C  N  N
               X  X  N  X  X                X  N  N  N  X
               X  X  X  X  X                X  X  N  X  X
    """

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
    for c in itertools.product(range(-range_, range_ + 1), repeat=dimension):
        if rule(c) and c != (0, ) * dimension:
            yield tuple(reversed(c))
