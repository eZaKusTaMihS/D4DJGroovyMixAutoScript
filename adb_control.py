import os
import subprocess
import recog
import numpy as np


btn_route = 'template\\ui\\btn'


def get_cur_screen(serial: str, screen_dir: str):
    execute('e: & cd e:/MuMuPlayer-12.0/shell & '
            'adb -s 127.0.0.1:%s exec-out screencap -p > %s' % (serial, screen_dir))


def click_btn(serial: str, btn: str):
    btn_data = recog.match('temp\\cur_screen.png', os.path.join(btn_route, btn))
    cx = np.random.randint(0, btn_data['width']) + btn_data['min_loc'][0]
    cy = np.random.randint(0, btn_data['height']) + btn_data['min_loc'][1]
    execute('e: & cd e:/MuMuPlayer-12.0/shell & '
            'adb -s 127.0.0.1:%s shell input tap %s %s' % (serial, cx, cy))
    print('click at position (%s, %s)' % (cx, cy))


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
