

class Controller:
    def __init__(self, rows_per_second):
        self.rows_per_second = rows_per_second
        self._row = 0
        self._playing = False
        self.connector = None

    @property
    def time(self):
        return self._row / self.rows_per_second

    @property
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, value):
        # Update other states..
        self._playing = value

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value
        self.connector.controller_row_changed(self._row)

    # Not all editors support this (breaks compatibility)
    # def pause(self):
    #     self._playing = not self._playing
    #     print("Pause:", not self._playing)
    #     self.connector.controller_pause_state(int(self._playing))

    def update(self):
        pass
