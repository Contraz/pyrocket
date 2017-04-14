from .socketconnector import SocketConnector
from .tracks import TrackContainer


class Rocket:
    def __init__(self, controller, track_path=None):
        self.controller = controller
        self.connector = None
        self.tracks = TrackContainer(track_path)
        # hack in reference so we can look up tracks_per_second
        self.tracks.controller = self.controller

    @property
    def time(self):
        return self.controller.time

    @property
    def row(self):
        return self.controller.row

    def start(self):
        self.connector = SocketConnector(controller=self.controller,
                                         tracks=self.tracks)
        # hack in references to avoid using callbacks for now
        self.tracks.connector = self.connector
        self.controller.connector = self.connector

    # Not all editors support this (breaks compatibility)
    # def pause(self):
    #     self.controller.pause()

    def update(self):
        self.controller.update()
        self.connector.update()

    def value(self, name):
        """get value of a track at the current time"""
        return self.tracks.get(name).row_value(self.controller.row)

    def int_value(self, name):
        return int(self.value(name))

    def track(self, name):
        return self.tracks.get_or_create(name)
