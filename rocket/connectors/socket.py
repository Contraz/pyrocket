import logging
import socket
import struct
from .base import Connector
import platform

logger = logging.getLogger("rocket")

CLIENT_GREET = "hello, synctracker!"
SERVER_GREET = "hello, demo!"

SYNC_DEFAULT_PORT = 1338

SET_KEY = 0
DELETE_KEY = 1
GET_TRACK = 2
SET_ROW = 3
PAUSE = 4
SAVE_TRACKS = 5
IS_WINDOWS = True if platform.system() == "Windows" else False


class SocketConnError(Exception):
    """Custom exception for detecting connection drop"""
    pass


class SocketConnector(Connector):
    """Connection to the rocket editor/server"""
    def __init__(self, host=None, port=None, controller=None, tracks=None):
        logger.info("Initializing socket connector")
        self.controller = controller
        self.tracks = tracks
        self.controller.connector = self
        self.tracks.connector = self

        self.host = host or "127.0.0.1"
        self.port = port or SYNC_DEFAULT_PORT

        self.socket = None
        self.reader = None
        self.writer = None

        self.init_socket()
        self.greet_server()

    def init_socket(self):
        logger.info("Attempting to connect to %s:%s", self.host, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        if IS_WINDOWS:
            self.socket.setblocking(False)
        else:
            self.socket.setblocking(True)
        logger.info("Connected to rocket server.")
        self.reader = BinaryReader(self.socket)
        self.writer = BinaryWriter(self.socket)

    def greet_server(self):
        logger.info("Greeting server with: %s", CLIENT_GREET)
        self.writer.string(CLIENT_GREET)
        greet = self.reader.bytes(len(SERVER_GREET))
        while greet is None:
            greet = self.reader.bytes(len(SERVER_GREET))
        data = greet.decode()
        logger.info("Server responded with: %s", data)
        if data != SERVER_GREET:
            raise ValueError("Invalid server response: {}".format(data))

    def track_added(self, name):
        self.writer.byte(GET_TRACK)
        self.writer.int(len(name))
        self.writer.string(name)

    def update(self):
        """Process all queued incoming commands"""
        while self.read_command():
            pass

    def controller_row_changed(self, row):
        self.writer.byte(SET_ROW)
        self.writer.int(int(row))
        logger.info(" <- row: %s", row)

    # # Not all editors support this (breaks compatibility)
    # def controller_pause_state(self, state):
    #     self.writer.byte(PAUSE)
    #     self.writer.byte(state)

    def read_command(self):
        """
        Attempt to read the next command from the editor/server
        :return: boolean. Did we actually read a command?
        """
        # Do a non-blocking read here so the demo can keep running if there is no data
        c = self.reader.byte(blocking=False)
        if c is None:
            return False
        cmds = {
            SET_KEY: self.handle_set_key,
            DELETE_KEY: self.handle_delete_key,
            SET_ROW: self.handle_set_row,
            PAUSE: self.handle_pause,
            SAVE_TRACKS: self.handle_save_tracks
        }
        func = cmds.get(c)
        if func:
            func()
        else:
            logger.error("Unknown command:", c)
        return True

    def handle_set_key(self):
        """Read incoming key from server"""
        track_id = self.reader.int()
        row = self.reader.int()
        value = self.reader.float()
        kind = self.reader.byte()
        logger.info(" -> track=%s, row=%s, value=%s, type=%s", track_id, row, value, kind)

        # Add or update track value
        track = self.tracks.get_by_id(track_id)
        track.add_or_update(row, value, kind)

    def handle_delete_key(self):
        """Read incoming delete key event from server"""
        track_id = self.reader.int()
        row = self.reader.int()
        logger.info(" -> track=%s, row=%s", track_id, row)

        # Delete the actual track value
        track = self.tracks.get_by_id(track_id)
        track.delete(row)

    def handle_set_row(self):
        """Read incoming row change from server"""
        row = self.reader.int()
        logger.info(" -> row: %s", row)
        self.controller.row = row

    def handle_pause(self):
        """Read pause signal from server"""
        flag = self.reader.byte()
        if flag > 0:
            logger.info(" -> pause: on")
            self.controller.playing = False
        else:
            logger.info(" -> pause: off")
            self.controller.playing = True

    def handle_save_tracks(self):
        logger.info("Remote export")
        self.tracks.save()


class BinaryReader:
    """Helper namespace for reading binary data from a socket"""
    def __init__(self, sock):
        self.sock = sock

    def bytes(self, n, blocking=True):
        return self._read(n, blocking=blocking)

    def byte(self, blocking=True):
        data = self._read(1, blocking=blocking)
        if data is None:
            return None
        return int.from_bytes(data, byteorder='big')

    def int(self, blocking=True):
        return struct.unpack('>I', self._read(4, blocking=blocking))[0]

    def float(self, blocking=True):
        return struct.unpack('>f', self._read(4, blocking=blocking))[0]

    def _read(self, count, blocking=True):
        try:
            if blocking:
                data = self.sock.recv(count)
            else:
                if IS_WINDOWS:
                    data = self.sock.recv(count)
                else:
                    data = self.sock.recv(count, socket.MSG_DONTWAIT)
        except BlockingIOError:
            return None

        if len(data) == 0:
            raise SocketConnError("Connection probably closed")
        return data


class BinaryWriter:
    """Helper for sending binary data"""
    def __init__(self, sock):
        self.sock = sock

    def byte(self, value):
        self.sock.send(value.to_bytes(1, byteorder='big', signed=False))

    def bytes(self, data):
        self.sock.write(data)

    def string(self, data):
        self.sock.send(data.encode())

    def int(self, value):
        self.sock.send(value.to_bytes(4, byteorder='big', signed=False))
