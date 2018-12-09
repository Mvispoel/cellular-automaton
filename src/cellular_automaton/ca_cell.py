class Cell:
    def __init__(self, name: str, coordinate: list):
        self.name = name
        self.coordinate = coordinate
        self.neighbours = []
        self.state = None
        self._dirty = False

    def set_neighbours(self, neighbours: list):
        """ Set new cells as neighbour of this cell.
        :param neighbours: A List of Cell names.
        """
        self.neighbours = neighbours

    def is_set_for_redrawing(self):
        return self._dirty

    def set_for_redraw(self):
        self._dirty = True

    def release_from_redraw(self):
        self._dirty = False
