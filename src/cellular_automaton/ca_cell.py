class Cell:
    def __init__(self, name: str):
        self.name = name
        self.neighbours = []

    def set_neighbours(self, neighbours: list):
        self.neighbours = neighbours
