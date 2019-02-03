from cellular_automaton.ca_cell import Cell, CellState
from cellular_automaton.ca_neighborhood import Neighborhood
from typing import Type


class Factory:
    def __init__(self):
        self._dimension = None
        self._state_class = None
        self._cells = {}

    def make_cellular_automaton(self,
                                dimension,
                                neighborhood: Type[Neighborhood],
                                state_class: Type[CellState]):
        self._dimension = dimension
        self._state_class = state_class

        self.__create_cells()
        self.__set_cell_neighbours(self._cells, neighborhood)
        return tuple(self._cells.values())

    def __create_cells(self, dimension_index=0, coordinate=None):
        """ Recursively steps down the dimensions to create cells in n dimensions and adds them to a dict.
        :param dimension_index:     The index indicating which dimension is currently traversed.
        :param coordinate:          The coordinate generated so far.
                                    (each recursion adds one dimension to the coordinate.
        """
        coordinate = _instantiate_coordinate_if_necessary(coordinate)

        try:
            self.__recursive_step_down_dimensions(coordinate, dimension_index)
        except IndexError:
            coordinate_string = _join_coordinate(coordinate)
            self._cells[coordinate_string] = Cell(self._state_class, coordinate)

    def __recursive_step_down_dimensions(self, coordinate, dimension_index):
        """ For the range of the current dimension, recalls the recursion method.
        :param coordinate:          The coordinate so far.
        :param dimension_index:     The current dimension lvl.
        """
        for cell_index in range(self._dimension[dimension_index]):
            new_cod = coordinate + [cell_index]
            self.__create_cells(dimension_index + 1, new_cod)

    def __set_cell_neighbours(self, cells, neighborhood):
        for cell in cells.values():
            n_coordinates = neighborhood.calculate_cell_neighbor_coordinates(cell.get_coordinate(),
                                                                             self._dimension)
            cell.set_neighbours([cells[_join_coordinate(coordinate)].get_state() for coordinate in n_coordinates])


def _instantiate_coordinate_if_necessary(coordinate):
    if coordinate is None:
        coordinate = []
    return coordinate


def _join_coordinate(coordinate):
    return '-'.join(str(x) for x in coordinate)

