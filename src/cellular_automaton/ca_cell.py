class Cell:
    def __init__(self, name: str, coordinate: list):
        self.name = name
        self.coordinate = coordinate
        self.neighbours = []
        self._status = [None, None]
        self._dirty = False

    def set_neighbours(self, neighbours: list):
        self.neighbours = neighbours

    def is_dirty(self):
        return self._dirty

    def set_dirty(self):
        self._dirty = True

    def release_dirty(self):
        self._dirty = False

    def set_status_for_iteration(self, new_status, iteration):
        """ Will set the new status for Iteration.
        :param new_status:  The new status to set.
        :param iteration:   Uses the iteration index, to differ between current and next state.
        :return True if status has changed.
        """
        self._status[iteration % 2] = new_status

        return self._status[0] != self._status[1]

    def get_status_for_iteration(self, iteration):
        """ Will return the status for the iteration.
        :param iteration:   Uses the iteration index, to differ between current and next state.
        :return The status for this iteration.
        """
        return self._status[iteration % 2]
