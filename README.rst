|pypi| |travis|

pyrocket
========

A `rocket <https://github.com/rocket/rocket>`__ client written in Python.

- The port was inspired by `Moonlander <https://github.com/anttihirvonen/moonlander>`_
- Tested with `Rocket OpenGL editor <https://github.com/emoon/rocket>`_

What is Rocket?
===============

Rocket is a sync-tracker tool for synchronizing music and visuals in demoscene productions.
It consists of an editor and a client that can either communicate with the editor over a
network socket, or play back an exported data-set.

This project is only a client (for now), so you will have to find an editor. You include
this client in your application so it can easily talk to an external editor or play back
key frame data in the final product.

Do note that the rocket system can also be used for other purposes were you need a static
set of interpolating key frames. There are no requirements for music to be involved.

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
  play it back. This is a perfectly valid option in the final product if you don't care
  that others can easily inspect and edit the project file and you are not constrained by
  file size limits. (Project files are xml with lots of additional metadata used by the editor)
- **Playback: Exported**: In editor mode you can select "export remote" that will tell
  the client to save all the current tracks in separate files in a binary format. This
  mode loads and plays back this data. The main purpose if this option is to vastly
  reduce the size of all the key frame data.


.. |pypi| image:: https://img.shields.io/pypi/v/pyrocket.svg
   :target: https://pypi.python.org/pypi/pyrocket
.. |travis| image:: https://travis-ci.org/Contraz/pyrocket.svg?branch=master
   :target: https://travis-ci.org/Contraz/pyrocket
