from abc import abstractmethod


class Rule:
    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def evolve_cell(last_cell_state, last_neighbour_states):
        """ Calculates and sets new state of 'cell'.
        :param last_cell_state:   The cells current state to calculate new state for.
        :param last_neighbour_states:  The cells neighbours current states.
        :return: True if state changed, False if not.
        A cells evolution will only be called if it or at least one of its neighbours has changed last iteration cycle.
        """
        return False
