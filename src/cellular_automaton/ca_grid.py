from cellular_automaton.ca_cell import CACell
from functools import reduce


class CAGrid:
    def __init__(self, dimensions, initial_grid_state=None):
        assert isinstance(dimensions, list)
        assert len(dimensions) > 0
        self._dimensions = dimensions

        self._cell_count = reduce(lambda x, y: x*y, dimensions)

        if initial_grid_state:
            assert isinstance(initial_grid_state, list)
            assert len(initial_grid_state) == self._cell_count
            assert isinstance(initial_grid_state[0], CACell)
            self._grid = initial_grid_state
        else:
            self._grid = []

            for i in range(self._cell_count):
                self._grid.append(CACell())

    def get_index_from_coordinate(self, coordinate):
        """ Convert a coordinate to the index in the grid list.
        :param coordinate:  A tuple or list with the position of the cell.
                            Has to have the same dimension as the grid.
        :return: The index of the cell at the coordinates
        """
        assert len(self._dimensions) == len(coordinate)
        index = 0
        for i, c in enumerate(coordinate[1:]):
            index += c * reduce(lambda x, y: x * y, self._dimensions[:i+1])
        index += coordinate[0]
        return index

    def get_coordinate_from_index(self, index):
        """ Convert an index to the coordinate in the grid list.
        :param index:       The Index of the cell in the grid.
        :return: The coordinate pointing at the indexed cell in the grid.
        """
        coordinate = len(self._dimensions)*[0]
        for i, d in enumerate(self._dimensions):
            coordinate[-(i + 1)] = index // reduce(lambda x, y: x * y, self._dimensions[-(i + 1):])
            index = index % reduce(lambda x, y: x * y, self._dimensions[-(i + 1):])

        coordinate[0] = index
        return coordinate

    def get_cell_by_coordinate(self, coordinate):
        """ Read a cell using a list or tuple as reference
        :param coordinate   A tuple or list with the position of the cell.
                            Has to have the same dimension as the grid.
        :return: The CACell at the coordinate in the grid.
        """
        try:
            return self[self.get_index_from_coordinate(coordinate)]
        except IndexError:
            return None

    def get_all_neighbour_cells(self, position, neighborhood):
        """ Get a list with all cells defined by the neighborhood.
        :param position:        The position as index or coordinate.
        :param neighborhood:    The neighborhood definition as tuple.
        :return: All Cells defined by the neighborhood in a list.
        """
        if isinstance(position, (tuple, list)):
            coordinate = position[:]
        else:
            coordinate = self.get_coordinate_from_index(position)

        neighbors = []

        for neighbor in neighborhood:
            neighbor_coordinate = []
            for i, (c, nc) in enumerate(zip(coordinate, neighbor)):
                coord = c + nc
                if coord < 0:
                    coord = self._dimensions[i] - 1
                elif coord == self._dimensions[i]:
                    coord = 0

                neighbor_coordinate.append(coord)

            index_ = self.get_cell_by_coordinate(neighbor_coordinate)
            if index_:
                neighbors.append(index_)

        return neighbors

    def get_dimensions(self):
        return self._dimensions

    def set_cell_by_coordinate(self, coordinate, value):
        """ Write to a cell using a list or tuple as reference
        :param coordinate   A tuple or list with the position of the cell.
                            Has to have the same dimension as the grid.
        """
        try:
            self._grid[self.get_index_from_coordinate(coordinate)] = value
        except IndexError:
            return None

    def __eq__(self, other):
        if len(self._grid) != len(other):
            return False

        for i in self._cell_count:
            if self._grid[i] != other[i]:
                return False

        return True

    def __len__(self):
        return len(self._grid)

    def __getitem__(self, index):
        return self._grid[int(index)]

    def __setitem__(self, index, value):
        self._grid[index] = value

    def __str__(self):
        return str(self._grid)
