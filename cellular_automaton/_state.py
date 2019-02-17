from cellular_automaton.cellular_automaton import Rule
from typing import Type


class CellularAutomatonState:
    def __init__(self, cells, dimension, evolution_rule: Type[Rule]):
        self.cells = cells
        self.dimension = dimension
        self.evolution_rule = evolution_rule
        self.current_evolution_step = -1
