from d4_control import D4Controller
import adb_control as adb


def main():
    serial = '16416'  # Emulator Serial (See your emulator config)
    # Connect adb
    adb.execute('e: & cd e:/MuMuPlayer-12.0/shell & adb.exe connect 127.0.0.1:%s' % serial)
    controller = D4Controller(serial)
    controller.start()


if __name__ == '__main__':
    main()
