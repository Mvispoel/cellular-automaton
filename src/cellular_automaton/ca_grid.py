import sys

from cellular_automaton.ca_cell import Cell
from cellular_automaton.ca_neighborhood import Neighborhood


class Grid:
    def __init__(self, dimension: list, neighborhood: Neighborhood):
        self._dimension = dimension
        self._cells = {}
        self._neighborhood = neighborhood

        self._create_cells()
        self._set_cell_neighbours()

        self._active_cells = self._cells.copy()
        self._set_all_cells_active()

    def get_names_of_active_cells(self):
        return list(self._active_cells.keys())

    def get_active_cells(self):
        return self._active_cells

    def clear_active_cells(self):
        self._active_cells.clear()

    def set_cell_and_neighbours_active(self, cell_info: list):
        self._active_cells[cell_info[0].name] = cell_info[0]
        for neighbour in cell_info[1]:
            self._active_cells[neighbour.name] = neighbour

    def get_cell_and_neighbors(self, cell_name):
        cell = self._cells[cell_name]
        neighbours = cell.neighbours
        neighbour_objects = []
        for ne in neighbours:
            neighbour_objects.append(self._cells[ne])

        return [cell, neighbour_objects]

    def get_cell_by_coordinate(self, coordinate):
        return self._cells[_join_coordinate(coordinate)]

    def get_dimension(self):
        return self._dimension

    def _set_all_cells_active(self):
        for cell_key, cell in self._cells.items():
            self._active_cells[cell_key] = cell

    def _create_cells(self, dimension_index=0, coordinate=None):
        """ Recursively steps down the dimensions to create cells in n dimensions and adds them to a dict.
        :param dimension_index:     The index indicating which dimension is currently traversed.
        :param coordinate:          The coordinate generated so far.
                                    (each recursion adds one dimension to the coordinate.
        """
        coordinate = _instantiate_coordinate_if_necessary(coordinate)

        try:
            self._recursive_step_down_dimensions(coordinate, dimension_index, self._create_cells)
        except IndexError:
            coordinate_string = _join_coordinate(coordinate)
            self._cells[coordinate_string] = Cell(coordinate_string, coordinate)

    def _recursive_step_down_dimensions(self, coordinate, dimension_index, recursion_method):
        """ For the range of the current dimension, recalls the recursion method.
        :param coordinate:          The coordinate so far.
        :param dimension_index:     The current dimension lvl.
        :param recursion_method:    The method to call for recursion.
        """
        for cell_index in range(self._dimension[dimension_index]):
            new_cod = coordinate + [cell_index]
            recursion_method(dimension_index + 1, new_cod)

    def _set_cell_neighbours(self, dimension_index=0, coordinate=None):
        """ Recursively steps down the dimensions to get the string instances for each cells neighbours.
        :param dimension_index:     The index indicating which dimension is currently traversed.
        :param coordinate:          The coordinate generated so far.
                                    (each recursion adds one dimension to the coordinate.
        """
        coordinate = _instantiate_coordinate_if_necessary(coordinate)

        try:
            self._recursive_step_down_dimensions(coordinate.copy(), dimension_index, self._set_cell_neighbours)
        except IndexError:
            neighbours_coordinates = self._neighborhood.get_neighbor_coordinates(coordinate, self._dimension)
            neighbour_names = [self._cells[_join_coordinate(nc)].name for nc in neighbours_coordinates]
            self._cells[_join_coordinate(coordinate)].set_neighbours(neighbour_names)

#    def __sizeof__(self):
#        size = 0
#        for cell in self._cells.values():
#            size += sys.getsizeof(cell)
#        size += sys.getsizeof(self._dimension) + sys.getsizeof(self._cells) + sys.getsizeof(self._active_cells)

#        return size


def _instantiate_coordinate_if_necessary(coordinate):
    if coordinate is None:
        coordinate = []
    return coordinate


def _join_coordinate(coordinate):
    return '-'.join(str(x) for x in coordinate)

