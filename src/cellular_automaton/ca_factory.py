from cellular_automaton import *
from typing import Type
import itertools


class CAFactory:
    @staticmethod
    def make_cellular_automaton(dimension,
                                neighborhood: Neighborhood,
                                state_class: Type[CellState],
                                rule: Type[Rule]):
        cells = CAFactory._make_cells(dimension, state_class)
        CAFactory._apply_neighborhood_to_cells(cells, neighborhood, dimension)
        return CellularAutomatonState(cells, dimension, rule)

    @staticmethod
    def _make_cells(dimension, state_class):
        cells = {}
        for c in itertools.product(*[range(d) for d in dimension]):
            cells[tuple(c)] = Cell(state_class)
        return cells

    @staticmethod
    def _apply_neighborhood_to_cells(cells, neighborhood, dimension):
        for coordinate, cell in cells.items():
            n_coordinates = neighborhood.calculate_cell_neighbor_coordinates(coordinate, dimension)
            cell.neighbor_states = [cells[tuple(nc)].state for nc in n_coordinates]

