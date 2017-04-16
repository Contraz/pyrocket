import time
from rocket.connectors import SocketConnError
from rocket.rocket import Rocket
from rocket.controllers import TimeController


def main():
    controller = TimeController(24)
    # rocket = Rocket.from_socket(controller)
    rocket = Rocket.from_project_file(controller, 'example.xml')
    rocket.start()

    rocket.track("underwater:cam.x")
    rocket.track("underwater:cam.y")
    t1 = rocket.track("cube:size")
    t2 = rocket.track("cube:zoom")

    # Fake draw loop
    frame = 0
    while True:
        try:
            rocket.update()
        except SocketConnError:
            print("Editor probably closed..")
            break

        # Get track values from rocket
        v1 = rocket.value("underwater:cam.x")
        v2 = rocket.value("underwater:cam.y")
        # Get track values from track
        v3 = t1.row_value(rocket.row)
        v4 = t2.row_value(rocket.row)

        time.sleep(1.0 / 1000 * 16)
        frame += 1

        if frame % 60 == 0:
            print("frame", frame, "time", rocket.time, "row", rocket.row, "playing", controller.playing)
            print("values", v1, v2, v3, v4)


if __name__ == '__main__':
    main()
