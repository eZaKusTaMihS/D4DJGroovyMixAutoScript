import os, time
import subprocess
from img_process import ImgProcessor
import numpy as np
import re

ip = ImgProcessor()


class AdbController:
    __btn_route = 'template\\ui\\btn'
    __lim = 1e-9

    serial = '127.0.0.1:16416'

    def __init__(self, btn_route: str = 'template\\ui\\btn', lim: float = 1e-9, serial='127.0.0.1:16416') -> None:
        self.__btn_route = btn_route
        self.__lim = lim
        self.serial = serial
        return

    def screenshot(self, screen_dir: str) -> bool:
        """
        Get screenshot and save it to ``screen_dir``
        :param screen_dir: The directory to save the screenshot to
        :return: Whether the screenshot was saved
        """
        # ct = time.time()
        return self.__execute(  # 'e: & cd e:/MuMuPlayer-12.0/shell & '
            'adb -s %s exec-out screencap -p > %s' % (self.serial, screen_dir))
        # print(time.time() - ct)

    def click_btn(self, btn: str, lim: float = __lim, do_screenshot: bool = True) -> bool:
        if not btn.endswith('.png'):
            # l = re.search(r'\.[a-z]*', btn)
            btn += '.png'
        cl_path = 'temp\\cur_screen.png'
        if do_screenshot:
            cl_path = 'temp\\cl_screen.png'
            self.screenshot(os.path.join(os.getcwd(), cl_path))
        btn_data = ip.match(cl_path, os.path.join(self.__btn_route, btn))
        if ip.matches_dt(btn_data, lim):
            return self.click(btn_data['min_loc'], btn_data['width'], btn_data['height'])
        return False

    def click(self, pos: tuple[int, int], width: int, height: int) -> bool:
        """
        Click randomly on a given area.
        :param pos: Starting position (upper left corner of the area)
        :param width: Width of the area
        :param height: Height of the area
        :return: Whether the click was successful or not
        """
        if width == 0:
            width = 1
        if height == 0:
            height = 1
        cx = np.random.randint(0, width) + pos[0]
        cy = np.random.randint(0, height) + pos[1]
        res = False
        try:
            res = self.__execute(  # 'e: & cd e:/MuMuPlayer-12.0/shell & '
                'adb -s %s shell input tap %s %s' % (self.serial, cx, cy))
            if res:
                print('mouse click @ (%s, %s)' % (cx, cy))
                time.sleep(0.3)
        except:
            pass
        finally:
            if not res:
                print('The click ain\'t successful.')
            return res

    def connect_device(self, serial: str = serial) -> bool:
        """
        Connect to adb device.
        :param serial: If provided, will change working serial and connect to this device.
        :return: Whether connection is successfully established.
        """
        self.serial = serial
        return self.__execute('adb connect %s' % self.serial)

    def __execute(self, statement: str) -> bool:
        """
        Executes command and prints the execution result.
        :param statement: The statement to execute.
        :return: Whether the statement is successfully executed.
        """
        p = subprocess.Popen(statement, shell=True, stdout=subprocess.PIPE)
        while p.poll() is None:
            if p.wait() != 0:
                print("Failed")
                return False
            else:
                re = p.stdout.readlines()
                for result in re:
                    print(result)
        return True
