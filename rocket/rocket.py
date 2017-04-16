from .connectors import SocketConnector
from .connectors import ProjectFileConnector
from .tracks import TrackContainer


class Rocket:
    def __init__(self, controller):
        """Create rocket instance without a connector"""
        self.controller = controller
        self.connector = None
        self.tracks = TrackContainer()
        # hack in reference so we can look up tracks_per_second
        self.tracks.controller = self.controller

    @staticmethod
    def from_project_file(controller, project_file):
        """Create rocket instance using project file connector"""
        rocket = Rocket(controller)
        rocket.connector = ProjectFileConnector(project_file,
                                                controller=controller,
                                                tracks=rocket.tracks)
        # hack in references to avoid using callbacks for now
        rocket.tracks.connector = rocket.connector
        rocket.controller.connector = rocket.connector
        return rocket

    @staticmethod
    def from_socket(controller, host=None, port=None):
        """Create rocket instance using socket connector"""
        rocket = Rocket(controller)
        rocket.connector = SocketConnector(controller=controller,
                                           tracks=rocket.tracks,
                                           host=host,
                                           port=port)
        # hack in references to avoid using callbacks for now
        rocket.tracks.connector = rocket.connector
        rocket.controller.connector = rocket.connector
        return rocket

    @property
    def time(self):
        return self.controller.time

    @property
    def row(self):
        return self.controller.row

    def start(self):
        self.controller.playing = True

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
