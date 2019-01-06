from cellular_automaton.ca_grid import Grid
from cellular_automaton.ca_rule import Rule
from cellular_automaton.ca_cell_state import CellState

from multiprocessing import Process, Pipe,  Array, Value
import multiprocessing


class CellularAutomaton:
    def __init__(self, grid: Grid, evolution_rule: Rule):
        self.grid = grid
        self.evolution_rule = evolution_rule
        self.evolution_iteration_index = 0


class _EvolutionProcess:
    def __init__(self, process: Process, pipe: Pipe):
        self.process = process
        self.pipe = pipe
        self.cell = None


class CellularAutomatonProcessor:
    def __init__(self, process_count: int = 1):
        self._processes = list(_create_processes(process_count))
        self.__cellular_automaton = None

    def evolve_x_times(self, cellular_automaton: CellularAutomaton, evolution_steps: int):
        """ Evolve all cells for x time steps.
        :param cellular_automaton: The cellular automaton to evolve.
        :param evolution_steps: The count of evolutions done.
        :return: True if all cells are inactive
        """
        for evo in range(evolution_steps):
            finished = self.evolve(cellular_automaton)
            if finished:
                return True
        return False

    def evolve(self, cellular_automaton: CellularAutomaton):
        """ Evolves all active cells for one time step.
        :param cellular_automaton: The cellular automaton to evolve.
        :return: True if all cells are inactive.
        """
        self.__cellular_automaton = cellular_automaton
        if self._is_evolution_finished():
            print("finished")
            return True
        else:
            cellular_automaton.evolution_iteration_index += 1
            self._evolve_all_active_cells()
            return False

    def _is_evolution_finished(self):
        return len(self.__cellular_automaton.grid.get_active_cell_names()) == 0

    def _evolve_all_active_cells(self):
        active_cells = self.__cellular_automaton.grid.get_active_cells()
        self.__cellular_automaton.grid.clear_active_cells()
        self._evolve_cells(active_cells.values())
        print(len(self.__cellular_automaton.grid.get_active_cells()))

    def _evolve_cells(self, cells):
        cellular_automaton = self.__cellular_automaton
        processes = self._processes
        process_count = len(processes)
        for i, cell in enumerate(cells):
            evolution_process = processes[i % process_count]
            if evolution_process.cell:
                response = evolution_process.pipe.recv()
                evolved_cell = evolution_process.cell
                evolved_cell.state = response[0]
                evolved_cell.is_set_for_redraw |= response[1]
                if evolved_cell.is_set_for_redraw:
                    cellular_automaton.grid.set_cells_active([evolved_cell] + evolved_cell.neighbours)
                evolution_process.cell = None

            cell_info = self.read_cell_info(cell, cellular_automaton.evolution_iteration_index)
            evolution_process.pipe.send(cell_info)
            evolution_process.cell = cell

        for evolution_process in processes:
            response = evolution_process.pipe.recv()
            cell = evolution_process.cell
            cell.state = response[0]
            cell.is_set_for_redraw |= response[1]
            if cell.is_set_for_redraw:
                cellular_automaton.grid.set_cells_active([cell] + cell.neighbours)
            evolution_process.cell = None

            # if cellular_automaton.evolution_rule.evolve_cell(cell.state, cellular_automaton.evolution_iteration_index):
            #     cellular_automaton.grid.set_cells_active([cell] + cell.neighbours)

    @staticmethod
    def read_cell_info(cell, iteration):
        coordinate = cell.coordinate
        return [coordinate, cell.state, [n.state for n in cell.neighbours], iteration]

        # if cell.state is not None:
        #     cell_state = cell.state.get_status_of_iteration(iteration - 1)
        # else:
        #     cell_state = None
        #
        # neighbor_states = []
        # for neighbor in cell.neighbours:
        #     if neighbor.state is not None:
        #         neighbor_state = neighbor.state.get_status_of_iteration(iteration - 1)
        #     else:
        #         neighbor_state = None
        #     neighbor_states.append(neighbor_state)
        #
        # return [coordinate,  cell_state, neighbor_states]


def _create_processes(count):
    for i in range(count):
        parent_pipe_connection, child_pipe_connection = Pipe()
        p = Process(target=process_routine, args=(child_pipe_connection, ))
        p.start()
        yield _EvolutionProcess(p, parent_pipe_connection)


def process_routine(pipe_conn: Pipe):
    while True:
        info = pipe_conn.recv()
        pipe_conn.send(evolve_cell(*info))


def evolve_cell(coordinate, cell_state, neighbor_states, index):
    if cell_state is None:
        return _init_state()
    else:
        new_state = _evolve_state(cell_state, neighbor_states, index)
        if new_state is None:
            print(",".join([str(x) for x in neighbor_states]))
            return [cell_state, False]
        else:
            changed = cell_state.set_status_of_iteration(new_state, index)
            return [cell_state, changed]


def _evolve_state(cell_state, neighbor_states, index):
    try:
        left_neighbour_state = neighbor_states[0].get_status_of_iteration(index - 1)
        return left_neighbour_state
    except (IndexError, AttributeError):
        return None


import random


def _init_state():
    rand = random.randrange(0, 101, 1)
    if rand <= 99:
        return [MyStatus(0), False]
    else:
        return [MyStatus(1), True]


class MyStatus(CellState):
    def __init__(self, initial_state):
        super().__init__(initial_state)

    def get_state_draw_color(self, iteration):
        red = 0
        if self._state_slots[iteration % 2][0]:
            red = 255
        return [red, 0, 0]

    def __str__(self):
        return super().__str__()
