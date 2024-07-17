import os
import subprocess
import recog
import numpy as np

btn_route = 'template\\ui\\btn'
m_lim = 1e-10


def get_cur_screen(serial: str, screen_dir: str):
    execute('e: & cd e:/MuMuPlayer-12.0/shell & '
            'adb -s %s exec-out screencap -p > %s' % (serial, screen_dir))


def click_btn(serial: str, btn: str, lim: float = m_lim) -> bool:
    btn_data = recog.match('temp\\cur_screen.png', os.path.join(btn_route, btn))
    if recog.matches_dt(btn_data, lim):
        click(serial, btn_data['min_loc'], btn_data['width'], btn_data['height'])
        return True
    return False


def click(serial: str, pos: tuple[int, int], width: int, height: int):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    cx = np.random.randint(0, width) + pos[0]
    cy = np.random.randint(0, height) + pos[1]
    execute('e: & cd e:/MuMuPlayer-12.0/shell & '
            'adb -s %s shell input tap %s %s' % (serial, cx, cy))
    print('mouse click @ (%s, %s)' % (cx, cy))


def execute(statement: str) -> bool:
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
