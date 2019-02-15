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
        return cells

    @staticmethod
    def _make_cells(dimension, state_class):
        cells = {}
        for c in itertools.product(*[range(d) for d in dimension]):
            cells[tuple(c)] = Cell(state_class)
        return cells

    @staticmethod
    def _apply_neighbourhood_to_cells(cells, neighborhood, dimension):
        for coordinate, cell in cells.items():
            n_coordinates = neighborhood.calculate_cell_neighbor_coordinates(coordinate, dimension)
            cell.neighbours = [cells[tuple(nc)].state for nc in n_coordinates]

