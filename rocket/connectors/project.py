"""
Connector reading tracks from the track editor xml file.
"""
import logging
import re
from xml.etree import ElementTree
from .base import Connector

logger = logging.getLogger("rocket")


class ProjectFileConnector(Connector):
    """Reads editor project xml file"""
    def __init__(self, project_file, controller=None, tracks=None):
        logger.info("Initializing project file loader")
        self.controller = controller
        self.tracks = tracks
        self.controller.connector = self
        self.tracks.connector = self

        logger.info("Attempting to load '%s'", project_file)

        with open(project_file, 'r') as fd:
            xml = fd.read()
        # Hack in a root node as ET expects only one root node
        root = ElementTree.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")
        tracks = root.find('tracks')

        # TODO: Consider using root attributes
        # root.attrib {'rows': '10000', 'startRow': '0', 'endRow': '10000', 'highlightRowStep': '8'}

        for track in tracks:
            t = self.tracks.get_or_create(track.attrib['name'])
            for key in track:
                t.add_or_update(
                    int(key.attrib['row']),
                    float(key.attrib['value']),
                    int(key.attrib['interpolation']))
            self.tracks.add(t)
