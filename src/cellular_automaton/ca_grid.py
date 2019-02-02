from cellular_automaton.ca_cell import Cell
from cellular_automaton.ca_neighborhood import Neighborhood


class Grid:
    def __init__(self, dimension: list, neighborhood: Neighborhood, state_class):
        self._dimension = dimension
        self._cells = {}
        self._active_cells = {}
        self._state_class = state_class

        self._init_cells(neighborhood)

    def _init_cells(self, neighborhood):
        self._create_cells()
        self._set_cell_neighbours(neighborhood)
        self._active_cells = self._cells.copy()
        self._set_all_cells_active()

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
            self._cells[coordinate_string] = Cell(self._state_class, coordinate)

    def _recursive_step_down_dimensions(self, coordinate, dimension_index, recursion_method):
        """ For the range of the current dimension, recalls the recursion method.
        :param coordinate:          The coordinate so far.
        :param dimension_index:     The current dimension lvl.
        :param recursion_method:    The method to call for recursion.
        """
        for cell_index in range(self._dimension[dimension_index]):
            new_cod = coordinate + [cell_index]
            recursion_method(dimension_index + 1, new_cod)

    def _set_cell_neighbours(self, neighborhood):
        for cell in self._cells.values():
            neighbours_coordinates = neighborhood.calculate_cell_neighbor_coordinates(cell.get_coordinate(),
                                                                                      self._dimension)
            cell.set_neighbours(list(map(self._get_cell_state_by_coordinate, neighbours_coordinates)))

    def _get_cell_state_by_coordinate(self, coordinate):
        return self._cells[_join_coordinate(coordinate)].get_state()

    def _set_all_cells_active(self):
        for cell_key, cell in self._cells.items():
            self._active_cells[cell_key] = cell

    def get_active_cell_names(self):
        return list(self._active_cells.keys())

    def get_active_cells(self):
        return self._active_cells

    def get_cells(self):
        return self._cells

    def get_dimension(self):
        return self._dimension


def _instantiate_coordinate_if_necessary(coordinate):
    if coordinate is None:
        coordinate = []
    return coordinate


def _join_coordinate(coordinate):
    return '-'.join(str(x) for x in coordinate)

