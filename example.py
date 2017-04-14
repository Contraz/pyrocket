import time
from rocket.socketconnector import SocketConnError
from rocket.rocket import Rocket
from rocket.controller import TimeController


def main():
    controller = TimeController(24)
    rocket = Rocket(controller, track_path="./data")
    rocket.start()

    rocket.track("underwater:cam.x")
    rocket.track("underwater:cam.y")
    t1 = rocket.track("cube:size")
    t2 = rocket.track("cube:zoom")

    # Fake draw loop
    frames = 0
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
        v3 = t1.value(rocket.row)
        v4 = t2.value(rocket.row)

        time.sleep(1.0 / 1000 * 16)
        frames += 1

        if frames % 60 == 0:
            print("T", rocket.time, "R", rocket.row, "P", controller.playing)
            print(v1, v2, v3, v4)
            print(frames)


if __name__ == '__main__':
    main()
