"""
Connector reading tracks from the track editor xml file.
"""
from xml.etree import ElementTree
from .base import Connector
from rocket.tracks import Track


class ProjectFileConnector(Connector):
    """Reads editor project xml file"""
    def __init__(self, project_file, controller=None, tracks=None):
        self.controller = controller
        self.tracks = tracks

        tree = ElementTree.parse(project_file)
        root = tree.getroot()

        # {'rows': '10000', 'startRow': '0', 'endRow': '10000', 'highlightRowStep': '8'}
        # print(root.attrib)

        for track in root:
            t = Track(track.attrib['name'])
            for key in track:
                t.add_or_update(
                    int(key.attrib['row']),
                    float(key.attrib['value']),
                    int(key.attrib['interpolation']))
            self.tracks.add(t)
