from enum import Enum


class EdgeRule(Enum):
    IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS = 0
    IGNORE_EDGE_CELLS = 1
    FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS = 2


class Neighborhood:
    def __init__(self, neighbors: list, edge_rule: EdgeRule):
        """ Defines a neighborhood for cells.
        :param neighbors: List of relative coordinates for the neighbors.
        :param edge_rule: A EdgeRule to define, how Cells on the edge of the grid will be handled.
        """
        self._neighbors = neighbors
        self.edge_rule = edge_rule
        self.grid_dimensions = []

    def calculate_cell_neighbor_coordinates(self, cell_coordinate, grid_dimensions):
        """ Get a list of coordinates for the cell neighbors. The EdgeRule can reduce the returned neighbor count.
        :param cell_coordinate:     The coordinate of the cell to get the neighbors
        :param grid_dimensions:          The dimensions of the grid, to apply edge the rule.
        :return:
        """
        self.grid_dimensions = grid_dimensions
        if self._does_ignore_edge_cell_rule_apply(cell_coordinate):
            return []
        else:
            return self._apply_edge_rule_to_neighbours(cell_coordinate)

    def _does_ignore_edge_cell_rule_apply(self, coordinate):
        if self.edge_rule == EdgeRule.IGNORE_EDGE_CELLS and self._is_coordinate_on_an_edge(coordinate):
            return True
        return False

    def _is_coordinate_on_an_edge(self, coordinate):
        for neighbor_dimension, dimension in zip(coordinate, self.grid_dimensions):
            if neighbor_dimension == 0 or neighbor_dimension == dimension - 1:
                return True
        return False

    def _apply_edge_rule_to_neighbours(self, coordinate):
        remaining_neighbours = []
        for neighbour in self._neighbors:
            if not self._does_ignore_edge_cell_neighbours_rule_apply(neighbour, coordinate):
                remaining_neighbours.append(self._calculate_neighbour_coordinate(neighbour, coordinate))
        return remaining_neighbours

    def _does_ignore_edge_cell_neighbours_rule_apply(self, neighbour, coordinate):
        if self.edge_rule == EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS:
            for rel_neighbour_dim, cell_dim, dim in zip(neighbour, coordinate, self.grid_dimensions):
                neighbor_dimension = cell_dim + rel_neighbour_dim
                if neighbor_dimension < 0 or neighbor_dimension >= dim:
                    return True
        return False

    def _calculate_neighbour_coordinate(self, neighbour, cell_coordinate):
        new_coordinate = []
        for rel_neighbour_dim, cell_dim, dim in zip(neighbour, cell_coordinate, self.grid_dimensions):
            neighbor_dim = cell_dim + rel_neighbour_dim
            neighbor_dim = self._calculate_neighbour_dimension_of_edge_cells(dim, neighbor_dim)
            new_coordinate.append(neighbor_dim)
        return new_coordinate

    @staticmethod
    def _calculate_neighbour_dimension_of_edge_cells(dim, neighbor_dim):
        if neighbor_dim < 0:
            neighbor_dim = dim - 1
        elif neighbor_dim >= dim:
            neighbor_dim = 0
        return neighbor_dim


class MooreNeighborhood(Neighborhood):
    def __init__(self, edge_rule: EdgeRule):
        super().__init__([[-1, -1], [0, -1], [1, -1],
                          [-1, 0], [1, 0],
                          [-1, 1], [0, 1], [1, 1]],
                         edge_rule)
