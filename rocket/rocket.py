import logging
from .connectors import SocketConnector
from .connectors import ProjectFileConnector
from .connectors import FilesConnector
from .tracks import TrackContainer

logger = logging.getLogger("rocket")


class Rocket:
    def __init__(self, controller, track_path=None, log_level=logging.ERROR):
        """Create rocket instance without a connector"""
        # set up logging
        sh = logging.StreamHandler()
        sh.setLevel(log_level)
        formatter = logging.Formatter('%(name)s-%(levelname)s: %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        logger.setLevel(log_level)

        self.controller = controller
        self.connector = None
        self.tracks = TrackContainer(track_path)
        # hack in reference so we can look up tracks_per_second
        self.tracks.controller = self.controller

    @staticmethod
    def from_files(controller, track_path, log_level=logging.ERROR):
        """Create rocket instance using project file connector"""
        rocket = Rocket(controller, track_path=track_path, log_level=log_level)
        rocket.connector = FilesConnector(track_path,
                                          controller=controller,
                                          tracks=rocket.tracks)
        return rocket

    @staticmethod
    def from_project_file(controller, project_file, track_path=None, log_level=logging.ERROR):
        """Create rocket instance using project file connector"""
        rocket = Rocket(controller, track_path=track_path, log_level=log_level)
        rocket.connector = ProjectFileConnector(project_file,
                                                controller=controller,
                                                tracks=rocket.tracks)
        return rocket

    @staticmethod
    def from_socket(controller, host=None, port=None, track_path=None, log_level=logging.ERROR):
        """Create rocket instance using socket connector"""
        rocket = Rocket(controller, track_path=track_path, log_level=log_level)
        rocket.connector = SocketConnector(controller=controller,
                                           tracks=rocket.tracks,
                                           host=host,
                                           port=port)
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
