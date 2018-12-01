#!/usr/bin/env python3

import tkinter

from cellular_automaton.cellular_automaton import CellularAutomaton
from cellular_automaton.ca_neighberhood import Neighborhood
from cellular_automaton.ca_rule import CARule
from cellular_automaton.ca_grid import CAGrid
from cellular_automaton.ca_cell import CACell

import datetime
import pygame

UPDATE_RATE = 10


class TkGUI:
    def __init__(self):
        self.root = tkinter.Tk()

        self.canvas = tkinter.Canvas(self.root)
        self.canvas.pack(padx=5, pady=5)

        self.ca = None
        self.current_state = None
        self.dimensions = None
        self.rule_ = None

        self.grid_image = None

    def run(self):
        self.root.after(10, self.update_state())
        self.root.mainloop()

    def update_state(self):
        a = datetime.datetime.now()
        self.current_state = self.ca.evolve(self.current_state, Neighborhood.MOOR_2_X_2, self.rule_)
        b = datetime.datetime.now()
        self.draw_current_state()
        c = datetime.datetime.now()
        print(b-a)
        print(c-b)
        self.root.after(UPDATE_RATE, self.update_state)

    def draw_current_state(self):
        for idx in range(self.dimensions[0]):
            for idy in range(self.dimensions[1]):
                cell = self.current_state[idy * self.dimensions[0] + idx]
                if cell[0] == 0:
                    cell_color = "#ffffff"
                else:
                    cell_color = "#444444"

                self.grid_image.put(cell_color, (idx, idy))

    def start(self, ca_, grid, dimensions, rule_):
        self.grid_image = tkinter.PhotoImage(width=dimensions[0], height=dimensions[1])
        self.ca = ca_
        self.current_state = grid
        self.dimensions = dimensions
        self.rule_ = rule_

        # Clear the canvas (remove all shapes)
        self.canvas.delete(tkinter.ALL)

        self.draw_current_state()
        self.canvas.create_image(self.dimensions, image=self.grid_image, state="normal")

        # Draw the canvas
        self.draw_current_state()


class TestRule(CARule):
    def evolve_cell(self, cell, neighbors):
        if neighbors[1][0] != 0:
            return [1]
        else:
            return [0]

#if __name__ == '__main__':
#    gui = TkGUI()
#   dim = [200, 500]
#    ca = CellularAutomaton(2)
#
#    new_grid = CAGrid(dim)
#    new_grid.set_cell_by_coordinate([1, 1], CACell([1]))
#    rule = TestRule()
#    gui.start(ca, new_grid, dim, rule)##
#
#    gui.run()
