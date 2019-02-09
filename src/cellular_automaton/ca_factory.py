from cellular_automaton.ca_cell import Cell, CellState
from cellular_automaton.ca_neighborhood import Neighborhood
from typing import Type
import itertools


class CAFactory:
    @staticmethod
    def make_cellular_automaton(dimension,
                                neighborhood: Type[Neighborhood],
                                state_class: Type[CellState]):

        cells = CAFactory._make_cells(dimension, state_class)
        CAFactory._apply_neighbourhood_to_cells(cells, neighborhood, dimension)
        return tuple(cells.values())

    @staticmethod
    def _make_cells(dimension, state_class):
        cells = {}
        for c in itertools.product(*[range(d) for d in dimension]):
            coordinate_string = _join_coordinate(c)
            cells[coordinate_string] = Cell(state_class, c)
        return cells

    @staticmethod
    def _apply_neighbourhood_to_cells(cells, neighborhood, dimension):
        for cell in cells.values():
            n_coordinates = neighborhood.calculate_cell_neighbor_coordinates(cell.get_coordinate(),
                                                                             dimension)
            cell.set_neighbours([cells[_join_coordinate(coordinate)].get_state() for coordinate in n_coordinates])


def _join_coordinate(coordinate):
    return '-'.join(str(x) for x in coordinate)

