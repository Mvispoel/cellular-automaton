# Cellular Automaton
This package provides an cellular automaton for [`Python® 3`](https://www.python.org/)

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
but when searching for one, I just found some minimalistic implementations,
that had little or no documentation with an API that really did not fit the problem
and Code that was desperately asking for some refactoring.

So I started to write my own module with the goal to provide an user friendly API
and acceptable documentation. During the implementation I figured, why not just provide 
n dimensional support and with reading Clean Code from Robert C. Martin the urge
to have a clean and tested code with a decent coverage added some more requirements.
The speed optimization and multi process capability was more of challenge for myself.
IMHO the module now reached an acceptable speed, but there is still room for improvements.

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
The module provides a pygame window for common two dimensional.
To add another kind of display option e.g. for other dimensions or hexagonal grids you can extrend the provided implementation or build you own.
The visual part of this module is fully decoupled and thus should be easily replaceable.

## Examples
The package contains two examples:
- [simple_star_fall](./examples/simple_star_fall.py)
- [conways_game_of_life](./examples/conways_game_of_life.py)

Those two example automaton implementations should provide a good start for your own automaton.

## Dependencies
As mentioned above the module depends on [pygame](https://www.pygame.org/news) for visualisation.
This is the only dependency however.