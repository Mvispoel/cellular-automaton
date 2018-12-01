#!/usr/bin/env python3

import pygame
import random

from cellular_automaton.cellular_automaton import CellularAutomaton
from cellular_automaton.ca_cell import CACell
from cellular_automaton.ca_grid import CAGrid
from cellular_automaton.ca_rule import CARule


class WorldGeneratorWindow:
    def __init__(self, windows_size):
        self.window_size = windows_size

        pygame.init()
        pygame.display.set_caption("World Generator")
        pygame.display.set_mode(self.window_size)

    def display_cellular_automaton(self, cellular_automaton_instance):
        pass


def main():

    running = True
    pygame.init()
    pygame.display.set_caption("minimal program")

    screen = pygame.display.set_mode((1000, 730))
    image = pygame.image.load("../images/map.png")
    screen.blit(image, (0, 0))
    screen.set_at((50, 60), [50, 0, 0])
    screen.set_at((50, 61), [50, 0, 0])
    screen.set_at((51, 60), [50, 0, 0])
    screen.set_at((51, 61), [50, 0, 0])
    pygame.display.flip()

    while running:
        for x in range(0, 1000):
            for y in range(0, 700):
                screen.set_at((x, y), [random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)])
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


class TestRule(CARule):
    def evolve_cell(self, cell, neighbors):
        if neighbors[1][0] != 0:
            return [1]
        else:
            return [0]


if __name__ == "__main__":
    main()
    dim = [200, 500]
    ca = CellularAutomaton(2)

    new_grid = CAGrid(dim)
    new_grid.set_cell_by_coordinate([1, 1], CACell([1]))
    rule = TestRule()
