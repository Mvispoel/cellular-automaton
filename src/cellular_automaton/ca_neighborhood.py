from enum import Enum
from operator import add


class EdgeRule(Enum):
    IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS = 0
    IGNORE_EDGE_CELLS = 1
    FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS = 2


class Neighborhood:
    def __init__(self, neighbours_relative: list, edge_rule: EdgeRule):
        """ Defines a neighborhood for cells.
        :param neighbours_relative: List of relative coordinates of cells neighbours.
        :param edge_rule: EdgeRule to define, how cells on the edge of the grid will be handled.
        """
        self._rel_neighbors = neighbours_relative
        self.edge_rule = edge_rule
        self.grid_dimensions = []

    def calculate_cell_neighbor_coordinates(self, cell_coordinate, grid_dimensions):
        """ Get a list of coordinates for the cell neighbors. The EdgeRule can reduce the returned neighbor count.
        :param cell_coordinate:     The coordinate of the cell to get the neighbors
        :param grid_dimensions:          The dimensions of the grid, to apply edge the rule.
        :return:
        """
        self.grid_dimensions = grid_dimensions
        return list(self._neighbours_generator(cell_coordinate))

    def _neighbours_generator(self, cell_coordinate):
        if not self._does_ignore_edge_cell_rule_apply(cell_coordinate):
            for rel_n in self._rel_neighbors:
                yield from self._calculate_abs_neighbour_and_decide_validity(cell_coordinate, rel_n)

    def _calculate_abs_neighbour_and_decide_validity(self, cell_coordinate, rel_n):
        n = list(map(add, rel_n, cell_coordinate))
        n_folded = self._apply_edge_overflow(n)
        if n == n_folded or self.edge_rule == EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS:
            yield n_folded

    def _does_ignore_edge_cell_rule_apply(self, coordinate):
        return self.edge_rule == EdgeRule.IGNORE_EDGE_CELLS and self._is_coordinate_on_an_edge(coordinate)

    def _is_coordinate_on_an_edge(self, coordinate):
        return all(0 == ci or ci == di-1 for ci, di in zip(coordinate, self.grid_dimensions))

    def _apply_edge_overflow(self, n):
        return list(map(lambda ni, di: (ni + di) % di, n, self.grid_dimensions))


class MooreNeighborhood(Neighborhood):
    def __init__(self, edge_rule: EdgeRule = EdgeRule.IGNORE_EDGE_CELLS):
        super().__init__([[-1, -1], [0, -1], [1, -1],
                          [-1, 0], [1, 0],
                          [-1, 1], [0, 1], [1, 1]],
                         edge_rule)
