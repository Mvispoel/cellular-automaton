from enum import Enum


class EdgeRule(Enum):
    IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS = 0
    IGNORE_EDGE_CELLS = 1
    FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS = 2


class CellularAutomatonNeighborhood:
    def __init__(self, neighbors: list, edge_rule: EdgeRule):
        self._neighbors = neighbors
        self.edge_rule = edge_rule
        self.dimensions = []

    def get_relative_neighbor_coordinates(self):
        return self._neighbors

    def get_neighbor_coordinates(self, cell_coordinate, dimensions):
        self.dimensions = dimensions
        if not self._does_ignore_edge_cell_rule_apply(cell_coordinate):
            return self._apply_edge_rule_to_neighbours_of(cell_coordinate)

    def _does_ignore_edge_cell_rule_apply(self, coordinate):
        if self.edge_rule == EdgeRule.IGNORE_EDGE_CELLS and self._is_coordinate_on_an_edge(coordinate):
            return True
        return False

    def _is_coordinate_on_an_edge(self, coordinate):
        for nd, d in zip(coordinate, self.dimensions):
            if nd == 0 or nd == d - 1:
                return True
        return False

    def _apply_edge_rule_to_neighbours_of(self, cell_coordinate):
        remaining_neighbours = []
        for neighbour in self._neighbors:
            if not self._does_ignore_edge_cell_neighbours_rule_apply(neighbour, cell_coordinate):
                remaining_neighbours.append(self._calculate_neighbour_coordinate(neighbour, cell_coordinate))

    def _does_ignore_edge_cell_neighbours_rule_apply(self, neighbour, cell_coordinate):
        if self.edge_rule == EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS:
            for rel_nd, cd, d in zip(neighbour, cell_coordinate, self.dimensions):
                nd = cd + rel_nd
                if nd < 0 or nd >= d:
                    return True
        return False

    def _calculate_neighbour_coordinate(self, neighbour, cell_coordinate):
        for rel_nd, cd, d in zip(neighbour, cell_coordinate, self.dimensions):
            nd = cd + rel_nd
            if nd < 0:
                nd = d - 1
            elif nd >= d:
                nd = 0
            return nd


class MooreNeighborhood(CellularAutomatonNeighborhood):
    def __init__(self, edge_rule: EdgeRule):
        super().__init__([[-1, -1], [0, -1], [1, -1],
                          [-1, 0], [0, 0], [1, 0],
                          [-1, 1], [0, 1], [1, 1]],
                         edge_rule)
