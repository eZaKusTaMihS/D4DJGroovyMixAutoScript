from d4_control import D4Controller
from adb_control import AdbController


def main():
    serial = '127.0.0.1:16416'  # Emulator Serial (See your emulator config)
    # Connect adb
    adb = AdbController(serial)
    adb.connect_device()
    # Start controller
    controller = D4Controller(serial)
    controller.start()


if __name__ == '__main__':
    main()
