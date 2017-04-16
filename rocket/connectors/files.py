"""
Connector reading track files in binary format.
Each track is a separate file.
"""
import os
from .base import Connector


class FilesConnector(Connector):
    """Loads individual track files in a specific path"""
    def __init__(self, path=None, controller=None, tracks=None):
        """
        Load binary track files
        :param path: Path to track directory
        :param controller: The controller
        :param tracks: Track container
        """
        self.controller = controller
        self.tracks = tracks
        self.path = path

        if not os.path.exists(self.path):
            raise IOError("Track directory do not exist: {}".format(self.path))

        # Find all track files and load them
        # ...
