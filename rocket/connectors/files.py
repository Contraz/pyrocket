"""
Connector reading track files in binary format.
Each track is a separate file.
"""
import logging
import os
from .base import Connector
from rocket.tracks import Track

logger = logging.getLogger("rocket")


class FilesConnector(Connector):
    """Loads individual track files in a specific path"""
    def __init__(self, track_path, controller=None, tracks=None):
        """
        Load binary track files
        :param path: Path to track directory
        :param controller: The controller
        :param tracks: Track container
        """
        logger.info("Initialize loading binary track data")
        self.controller = controller
        self.tracks = tracks
        self.path = track_path

        self.controller.connector = self
        self.tracks.connector = self

        if self.path is None:
            raise ValueError("track path is None")
        if not os.path.exists(self.path):
            raise ValueError("Track directory do not exist: {}".format(self.path))

        logger.info("Looking for track files in '%s'", self.path)
        for f in os.listdir(self.path):
            if not f.endswith(".track"):
                continue
            name = Track.trackname(f)
            logger.info("Attempting to load ''", name)
            t = self.tracks.get_or_create(name)
            t.load(os.path.join(self.path, f))
