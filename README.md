# Cellular Automaton
This package provides an cellular automaton for [Python 3](https://www.python.org/)

A cellular automaton defines a grid of cells and a set of rules.
All cells then evolve their state depending on their neighbours state simultaneously.

For further information on cellular automatons consult e.g. [mathworld.wolfram.com](http://mathworld.wolfram.com/CellularAutomaton.html)

## Yet another cellular automaton module?
It is not the first python module to provide a cellular automaton, 
but it is to my best knowledge the first that provides all of the following features:
 - easy to use
 - n dimensional
 - multi process capable
 - speed optimized
 - documented
 - tested
 
I originally did not plan to write a new cellular automaton module, 
but when searching for one, I just found some that had little or no documentation with an API that really did not fit my requirements
and/or Code that was desperately asking for some refactoring.

So I started to write my own module with the goal to provide an user friendly API
and acceptable documentation. During the implementation I figured, why not just provide 
n dimensional support and with reading Clean Code from Robert C. Martin the urge
to have a clean and tested code with a decent coverage added some more requirements.
The speed optimization and multi process capability was more of challenge for myself.
IMHO the module now reached an acceptable speed, but there is still room for improvements (e.g. with Numba?).

## Installation
This module can be loaded and installed from [pipy](https://pypi.org/project/cellular-automaton/): `pip install cellular-automaton`

## Usage
To start and use the automaton you will have to define three things:
- The neighborhood
- The dimensions of the grid
- The evolution rule

`````python
neighborhood = MooreNeighborhood(EdgeRule.IGNORE_EDGE_CELLS)
ca = CAFactory.make_single_process_cellular_automaton(dimension=[100, 100],
                                                      neighborhood=neighborhood,
                                                      rule=MyRule)
``````

### Neighbourhood
The Neighborhood defines for a cell neighbours in relative coordinates.
The evolution of a cell will depend solely on those neighbours.
 
The Edge Rule passed as parameter to the Neighborhood defines, how cells on the edge of the grid will be handled.
There are three options:
- Ignore edge cells: Edge cells will have no neighbours and thus not evolve.
- Ignore missing neighbours: Edge cells will add the neighbours that exist. This results in varying count of neighbours on edge cells.
- First and last cell of each dimension are neighbours: All cells will have the same neighbour count and no edge exists.

### Dimension
A list or Tuple which states each dimensions size.
The example above defines a two dimensional grid with 100 x 100 cells.

There is no limitation in how many dimensions you choose but your memory and processor power.

### Rule
The Rule has three tasks:
- Set the initial value for all cells.
- Evolve a cell in respect to its neighbours.
- (optional) define how the cell should be drawn.

`````python
class MyRule(Rule):

    def init_state(self, cell_coordinate):
        return (1, 1)

    def evolve_cell(self, last_cell_state, neighbors_last_states):
        return self._get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, -1))

    def get_state_draw_color(self, current_state):
        return [255 if current_state[0] else 0, 0, 0]
`````

Just inherit from `cellular_automaton.rule:Rule` and define the evolution rule and initial state.

## Visualisation
The package provides a module for visualization in a pygame window for common two dimensional automatons.

To add another kind of display option e.g. for other dimensions or hexagonal grids you can extrend the provided implementation or build your own.
The visual part of this module is fully decoupled and thus should be easily replaceable.

## Examples
The package contains two examples:
- [simple_star_fall](https://gitlab.com/DamKoVosh/cellular_automaton/-/tree/master/examples/simple_star_fall.py)
- [conways_game_of_life](https://gitlab.com/DamKoVosh/cellular_automaton/-/tree/master/examples/conways_game_of_life.py)

Those example automaton implementations should provide a good start for your own project.

## Getting Involved
Feel free to open pull requests, send me feature requests or even join as developer.
There ist still quite some work to do.

And for all others, don't hesitate to open issues when you have problems!

## Dependencies
For direct usage of the cellular automaton ther is no dependency.
If you want to use the display option however or execute the examples you will have to install 
[pygame](https://www.pygame.org/news) for visualisation.
If you do for some reason not want to use this engine simply inherit from display.DrawEngine and overwrite the 
necessary methods. (for an example of how to do so see ./test/test_display.py)

## Licence
This package is distributed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0), see [LICENSE.txt](https://gitlab.com/DamKoVosh/cellular_automaton/-/tree/master/LICENSE.txt)