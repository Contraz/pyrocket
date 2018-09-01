|pypi| |travis|

pyrocket
========

A `rocket <https://github.com/rocket/rocket>`__ client written in Python.

- The port was inspired by `Moonlander <https://github.com/anttihirvonen/moonlander>`_
- Tested with `Rocket OpenGL editor <https://github.com/emoon/rocket>`_

This project is written in python 3 and is verified to work on
Windows, OS X and Linux.

|editor|

pyrocket was originally part of demosys-py_ and was separated into this project.
The screenshot shows pyrocket with demosys-py and Rocket OpenGL editor.

What is Rocket?
===============

Rocket is a sync-tracker tool originally for synchronizing music and visuals in
demoscene productions, but has later also be used for many other purposes where
static sets of interpolating key frames are neeed. There are no requirements for
music to be involved.

It consists of an editor and a client that can either communicate
with the editor over a network socket, or play back an exported data-set.

This project is only a client (for now), so you will have to find an editor. You include
this client in your application so it can easily talk to an external editor or play back
existing key frame data from file(s).

Hardcoding this data is doable, but when reaching a certain complexity it can get ugly
pretty quick. Several datasets of keyframes can also be used in the same application
to play back some static or semi-static snippet of events and interpolations.

Converting other types of data and formats to rocket is also a use case
as the rocket format is very simple and accessible and requires fairly little
effort to include in your application.

Contributing
============

Be free to post questions and create issues. Do not hesitate to open a pull request
(completed or work in progress). The worst thing that can happen is that we learn something.

Contributors:

- `Einar Forselv <https://github.com/einarf>`_
- `Arttu Tamminen <https://github.com/helgrima>`_

How Rocket Works
================

Rocket data is a collection of named groups ("tracks") containing key frames. Each key
frame contains a row number (int), value (float) and interpolation type (enum/byte).
The row number is a time unit. This is translated to seconds based on a configured rows
per second value. Rows per second is normally adjusted based on the music such as beats
per minute. The row resolution will then be a grid that helps the user to place key
frames accurately in sync with the music.

The rocket client can be used in three different modes:

- **Editor mode**: Use the socket connector to connect to an external editor. The editor
  should ideally already be opened and you have loaded an xml file containing all the key
  frame data. When the client connects it will download all the key frames from the editor
  and will keep synchronizing the data as you edit the key frames.
- **Playback: Editor Data**: The client will load the xml file created by the editor and
  play it back. This is a perfectly valid option if the xml project file has a reasonable
  size. This is the commonly used option.
- **Playback: Exported**: In editor mode you can select "export remote" that will tell
  the client to save all the current tracks in separate files in a binary format. This
  mode loads and plays back this data. The main purpose of this option is to vastly
  reduce the size of all the key frame data if your xml project file gets unreasonably big.
  It can also add some obfuscation to your data.

Interpolation Types
===================

The client library will do all the interpolation calculations for you.
The rocket protocol is supposed to be as simple as possible. If you need any other
interpolation types you can for example use linear interpolation and apply
a formula on these values.

Supported interpolation modes are:
 - Step: Key frame produces a constant value)
 - Linear: Linear interpolation between key frames
 - Smooth: Interpolates key frames using: ``t * t * (3 - 2 * t)``
 - Ramp: Interpolates key frame using: ``t^2``

Using the Client
================

First of all you need a controller. This class keeps track of the current
time. We currently only implement a basic ``TimeController``. If you want music
playback you will have to implement your own controller by extending the base
``Controller`` class. The reason for this is simply that we don't want to lock
users into using a specific library.

When setting up a rocket project it's important to chose the right ``rows_per_second``.
This is the resolution of your key frame data.

If music is involved we calculate a resolution that would fit the beats
per minute. For 120 bpm music it may only be enough to use an rps of
20, 24 or 30.

Quick draw loop setup:

(Do note that both time and track row is interpolated as floats,
so even low values for ``rows_per_second`` will yield smoothly interpolated
key frame values)

.. code:: python

    import time
    from rocket import Rocket
    from rocket.controllers import TimeController

    # Simple controller tracking time at 24 rows per second (50ms resolution)
    controller = TimeController(20)

    # Below is the tree different ways to initialize the client

    # Editor mode (track_path: where binary track data ends up when doing a remote export)
    rocket = Rocket.from_socket(controller, track_path="./data")

    # Playback using the editor file
    rocket = Rocket.from_project_file(controller, 'example.xml')

    # Playback using binary track data
    rocket = Rocket.from_files(controller, './data')

    # Register some tracks
    # Just register a track
    rocket.track("cube:rotation")
    # Register a track and store the reference for later
    size_track = rocket.track("cube:size")

    # Enter the draw loop
    rocket.start()
    while True:
        # Update inner states. The controller is mainly involved in that.
        rocket.update()

        # Get the cube rotation value at the current time (when update() was last called)
        cube_rot = rocket.value("cube:rotation")

        # Get the cube size by accessing the track directly (using second)
        # This can be the value from your own timer as well
        cube_size = size_track.time_value(rocket.time)

        # Get the cube size by accessing the track directly (using track time)
        # This can be the value from your own timer as well
        cube_size = size_track.track_value(rocket.track)

        # Emulate 60 fps
        time.sleep(1.0 / 1000 * 16)

Track Names
===========

The standard rocket editor support track names using utf-8, but this is not a 100%
guarantee that other track editors also support this.

Some editors such as `Rocket OpenGL editor <https://github.com/emoon/rocket>`_
support track grouping. Grouping is done by adding a prefix in the track name
followed by a colon.

Example:
::

    cube:rot.x
    cube:rot.y
    cube:rot.z

    monkey:rot.x
    monkey:rot.y
    monkey:rot.z

The uniqueness of the track is based on the entire name, so you can re-use
the same name across different groups.

Track names (after colon) should ideally be as short as possible. 12 characters is
a good limit as editors either cut off the name or expand the column width with
larger names. It's common to use dot as a separator in track names as well, but
this is not enforced as far as we know.

When tracks are serialized into binary format the colon is replaced with #.
``cube:rot.x`` track is save in the file ``cube#rot.x.track``.

Logging
=======

The default log level of the client is ``ERROR``.

You can override the log level when initializing rocket:

.. code:: python

    import logging

    rocket = Rocket.from_socket(controller, track_path="./data", log_level=logging.INFO)
    rocket = Rocket.from_project_file(controller, 'example.xml', log_level=logging.INFO)
    rocket = Rocket.from_files(controller, './data', log_level=logging.INFO)

When adding custom controllers you can emit to the rocket logger:

.. code:: python

    import logging
    from rocket.controllers import Controller

    logger = logging.getLogger("rocket")

    class MyController(Controller):
        def __init__(self, rows_per_second):
            logger.info("Hello, Rocket!")

Format
======

Interpolation enum:

... code:: python

    STEP = 0
    LINEAR = 1
    SMOOTH = 2
    RAMP = 3

The xml format is very simple. The example below shows three tracks containing a few keyframes.

.. code:: xml

    <?xml version="1.0" ?>
    <tracks>
        <track name="camera:fov">
            <key interpolation="1" row="0" value="60.0"/>
            <key interpolation="1" row="40" value="90.0"/>
        </track>
        <track name="camera:head">
            <key interpolation="2" row="0" value="10.0"/>
            <key interpolation="2" row="100" value="40.0"/>
            <key interpolation="2" row="200" value="-20.0"/>
        </track>
        <track name="camera:pitch">
            <key interpolation="2" row="0" value="10.0"/>
            <key interpolation="2" row="200" value="20.0"/>
            <key interpolation="3" row="300" value="30.0"/>
        </track>
    </tracks>

The binary format is also fairly straight forward. Each track is written to
a separate file. These files should ideally be separated into their own directory.
The file name is ``<track_name>.track``.

The track names above would be:

.. code::

    tracks/camera#fov.track
    tracks/camera#head.track
    tracks/camera#pitch.track

The format of each track file is (all big endian):

.. code:

    int: number of keyframes
    for number of keyframes
        int: row
        float32: value
        byte: interpolation type

.. |editor| image:: https://raw.githubusercontent.com/Contraz/pyrocket/master/editor.png
.. |pypi| image:: https://img.shields.io/pypi/v/pyrocket.svg
   :target: https://pypi.python.org/pypi/pyrocket
.. |travis| image:: https://travis-ci.org/Contraz/pyrocket.svg?branch=master
   :target: https://travis-ci.org/Contraz/pyrocket
.. _demosys-py: https://github.com/Contraz/demosys-py
