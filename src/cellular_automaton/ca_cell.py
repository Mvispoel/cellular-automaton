class CACell:
    def __init__(self, initial_state=None):
        if initial_state:
            assert isinstance(initial_state, (tuple, list))
            self._state = initial_state
        else:
            self._state = [0]

    def __getitem__(self, index):
        return self._state[index]

    def __setitem__(self, index, value):
        self._state[index] = value

    def __len__(self):
        return len(self._state)

    def __str__(self):
        return str(self._state)
