import bisect
import math
# import os

STEP = 0
LINEAR = 1
SMOOTH = 2
RAMP = 3


class TrackContainer:
    """Keep track of tacks by their name and index"""
    def __init__(self, track_path):
        self.tracks = {}
        self.track_index = []
        self.connector = None
        self.controller = None
        self.track_path = track_path

    def get(self, name):
        return self.tracks[name]

    def get_by_id(self, i):
        return self.track_index[i]

    def get_or_create(self, name):
        t = self.tracks.get(name)
        if not t:
            t = Track(name)
            self.add(t)

        self.connector.track_added(name)
        return t

    def add(self, obj):
        """Add pre-created tracks"""
        obj.controller = self.controller
        self.tracks[obj.name] = obj
        self.track_index.append(obj)

    def save(self):
        for t in self.track_index:
            print("Saving", t.name)


# TODO: Insert and delete operations in keys list is expensive
class Track:
    def __init__(self, name):
        self.name = name
        self.keys = []
        # Shortcut to controller for tracks_per_second lookups
        self.controller = None

    def time_value(self, time):
        return self.row_value(time * self.controller.rows_per_second)

    def row_value(self, row):
        """Get the tracks value at row"""
        irow = int(row)
        i = self._get_key_index(irow)
        if i == -1:
            return 0.0

        # Are we dealing with the last key?
        if i == len(self.keys) - 1:
            return self.keys[-1].value

        return TrackKey.interpolate(self.keys[i], self.keys[i + 1], row)

    def add_or_update(self, row, value, kind):
        """Add or update a track value"""
        i = bisect.bisect_left(self.keys, row)

        # Are we simply replacing a key?
        if i < len(self.keys) and self.keys[i].row == row:
            self.keys[i].update(value, kind)
        else:
            self.keys.insert(i, TrackKey(row, value, kind))

    def delete(self, row):
        """Delete a track value"""
        i = self._get_key_index(row)
        del self.keys[i]

    def _get_key_index(self, row):
        """Get the key that should be used as the first interpolation value"""
        # Don't bother with empty tracks
        if len(self.keys) == 0:
            return -1

        # No track values are defined yet
        if row < self.keys[0].row:
            return -1

        # Get the insertion index
        index = bisect.bisect_left(self.keys, row)
        # Index is within the array size?
        if index < len(self.keys):
            # Are we inside an interval?
            if row < self.keys[index].row:
                return index - 1
            return index

        # Return the last index
        return len(self.keys) - 1

    def print_keys(self):
        for k in self.keys:
            print(k)


class TrackKey:
    def __init__(self, row, value, kind):
        self.row = row
        self.value = value
        self.kind = kind

    def update(self, value, kind):
        self.value = value
        self.kind = kind

    @staticmethod
    def interpolate(first, second, row):
        t = (row - first.row) / (second.row - first.row)

        if first.kind == STEP:
            return first.value
        elif first.kind == SMOOTH:
            t = t * t * (3 - 2 * t)
        elif first.kind == RAMP:
            t = math.pow(t, 2.0)

        return first.value + (second.value - first.value) * t

    def __lt__(self, other):
        if isinstance(other, int):
            return self.row < other
        else:
            return self.row < other.row

    def __ge__(self, other):
        if isinstance(other, int):
            return self.row > other
        else:
            return self.row > other.row

    def __repr__(self):
        return "TrackKey(row={} value={} type={})".format(self.row, self.value, self.kind)
