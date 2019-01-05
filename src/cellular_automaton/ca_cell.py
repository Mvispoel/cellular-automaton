class Cell:
    def __init__(self, name, coordinate: list):
        self.name = name
        self.coordinate = coordinate
        self.neighbours = []
        self.state = None
        self.is_set_for_redraw = False
