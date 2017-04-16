import time
from .base import Controller


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
