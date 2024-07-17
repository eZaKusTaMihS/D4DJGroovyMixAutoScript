import os, time
import recog
import adb_control as adb
import numpy as np

page_route = 'template\\ui\\pages'


def get_screen() -> str:
    sc_path = os.path.join(os.getcwd(), 'temp\\cur_screen.png')
    adb.get_cur_screen('16416', sc_path)
    return sc_path
    # return 'template\\select.png'


class D4Controller:
    screen = None
    serial = '16416'
    pages = ['okpop', 'closepop', 'again', 'select', 'prepare', 'live', 'bingo', 'network_err', 'dl', 'loading',
             'livein', 'main', 'next']
    cur_page = "none"
    voltage = 0
    event_pt = 0

    def __init__(self, serial='16416'):
        self.serial = serial

    def get_stat(self) -> dict:
        self.update_stat()
        return {
            "cur_page": self.cur_page,
            "voltage": self.voltage,
            "event_pt": self.event_pt
        }

    def update_stat(self) -> None:
        self.screen = get_screen()
        min_val = 100
        min_page = 'none'
        for page_name in self.pages:
            p_path = os.path.join(page_route, page_name)
            if not os.path.exists(p_path):
                continue
            cnt, min_v = 1, 0
            for i in os.listdir(p_path):
                min_v += abs(recog.match(self.screen, os.path.join(p_path, i))['min_val'])
            min_v /= cnt
            if min_v < 1e-9 and min_v < min_val:
                min_val = min_v
                min_page = page_name
        self.cur_page = min_page
        print(self.cur_page)

    def react_page(self, page: str):
        # Handle Unexpected situations
        if page == 'loading':
            time.sleep(1)
            return
        if page == 'network_err':
            print('Network Error.')
            time.sleep(4)
            return
        if page == 'closepop':
            adb.click_btn(self.serial, 'close.png')
            return
        if page == 'okpop':
            adb.click_btn(self.serial, 'ok.png')
            return
        # Process normal pages
        if page == 'select':
            if not recog.matches(self.screen, 'template\\content\\select\\akeba.png'):
                adb.click_btn(self.serial, 'akeba.png')
                time.sleep(0.3)
            adb.click_btn(self.serial, 'select.png')
            return
        if page == 'main':
            adb.click_btn(self.serial, 'golive.png')
            return
        if page == 'next':
            adb.click_btn(self.serial, 'next.png')
            return
        if page == 'prepare':
            adb.click_btn(self.serial, 'start.png')
            return
        if page == 'again':
            adb.click_btn(self.serial, 'again.png')
            time.sleep(2)
            return
        if page == 'bingo':
            adb.click_btn(self.serial, 'pok.png')
            return
        if page == 'livein':
            adb.click_btn(self.serial, 'livein.png')
            return
        if page == 'live':
            time.sleep(5)
            return
        adb.click(self.serial, (1620, 980), 50, 30)

    def start(self):
        while True:
            self.update_stat()
            print('current status: %s' % self.cur_page)
            self.react_page(self.cur_page)
            time.sleep(np.random.random() + 0.2)
