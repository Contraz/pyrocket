import time


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


class TimeController(Controller):
    def __init__(self, rows_per_second):
        self.last_meter_point = 0
        super().__init__(rows_per_second)

    def update(self):
        if not self.playing:
            self.last_meter_point = 0
            return

        if self.last_meter_point == 0:
            self.last_meter_point = time.time()

        meter = time.time()
        timespan = meter - self.last_meter_point
        self.last_meter_point = meter
        self.row = self.row + timespan * self.rows_per_second
