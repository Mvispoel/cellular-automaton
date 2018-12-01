from cellular_automaton.ca_cell import Cell
from cellular_automaton.ca_neighborhood import CellularAutomatonNeighborhood


class Grid:
    def __init__(self, dimension: list, neighborhood: CellularAutomatonNeighborhood):
        self._dimension = dimension
        self._cells = {}
        self._neighborhood = neighborhood

        self._create_cells()
        self._set_cell_neighbours()

        self._active_cells = {}
        self.set_all_cells_active()

    def set_all_cells_active(self):
        for cell_key in self._cells:
            self._active_cells[cell_key] = 1

    def get_active_cells(self):
        return self._active_cells.keys()

    def get_cell_and_neighbors(self, cell_name):
        cell = self._cells[cell_name]
        neighbours = cell.neighbours
        neighbour_objects = []
        for ne in neighbours:
            neighbour_objects.append(self._cells[ne])

        return [cell, neighbour_objects]


    def _create_cells(self, dimension_index=0, coordinate=None):
        """ Recursively steps down the dimensions to create cells in n dimensions and adds them to a dict.
        :param dimension_index:     The index indicating which dimension is currently traversed.
        :param coordinate:          The coordinate generated so far.
                                    (each recursion adds one dimension to the coordinate.
        """
        coordinate = self.instantiate_coordinate_if_necessary(coordinate)

        try:
            self._recursive_step_down_dimensions(coordinate, dimension_index, self._create_cells)
        except IndexError:
            coordinate_string = '-'.join(coordinate)
            self._cells[coordinate_string] = Cell(coordinate_string)

    def _recursive_step_down_dimensions(self, coordinate, dimension_index, recursion_method):
        """ For the range of the current dimension, recalls the recursion method.
        :param coordinate:          The coordinate so far.
        :param dimension_index:     The current dimension lvl.
        :param recursion_method:    The method to call for recursion.
        """
        for cell_index in range(self._dimension[dimension_index]):
            coordinate.append(cell_index)
            recursion_method(dimension_index + 1, coordinate.copy())

    @staticmethod
    def instantiate_coordinate_if_necessary(coordinate):
        if coordinate is None:
            coordinate = []
        return coordinate

    def _set_cell_neighbours(self, dimension_index=0, coordinate=None):
        """ Recursively steps down the dimensions to get the string instances for each cells neighbours.
        :param dimension_index:     The index indicating which dimension is currently traversed.
        :param coordinate:          The coordinate generated so far.
                                    (each recursion adds one dimension to the coordinate.
        """
        coordinate = self.instantiate_coordinate_if_necessary(coordinate)

        try:
            self._recursive_step_down_dimensions(coordinate, dimension_index, self._set_cell_neighbours)
        except IndexError:
            neighbours_coordinates = self._neighborhood.get_neighbor_coordinates(coordinate, self._dimension)
            neighbour_names = [self._cells['-'.join(nc)].name for nc in neighbours_coordinates]
            self._cells['-'.join(coordinate)].set_neighbours(neighbour_names)

