import os, time
import recog
import adb_control as adb
import numpy as np

page_route = 'template\\ui\\pages'


def get_screen() -> str:
    sc_path = os.path.join(os.getcwd(), 'temp\\cur_screen.png')
    adb.get_cur_screen('16416', sc_path)
    return sc_path


class D4Controller:
    serial = '16416'
    pages = ['okpop', 'closepop', 'fin', 'again', 'select', 'prepare', 'live', 'bingo', 'network_err', 'dl', 'loading']
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
        screen = get_screen()
        min_val = 100
        min_page = 'none'
        for page_name in self.pages:
            p_path = os.path.join(page_route, page_name)
            if not os.path.exists(p_path):
                continue
            cnt, min_v = 1, 0
            for i in os.listdir(p_path):
                min_v += abs(recog.match(screen, os.path.join(p_path, i))['min_val'])
            min_v /= cnt
            if min_v < 1e-9 and min_v < min_val:
                min_val = min_v
                min_page = page_name
        self.cur_page = min_page
        print(self.cur_page)

    def start(self):
        while True:
            time.sleep(np.random.random() + 0.8)
            self.update_stat()
            print('current status: %s' % self.cur_page)
            if self.cur_page == 'fin':
                adb.click_btn(self.serial, 'next.png')
            elif self.cur_page == 'loading':
                print('Suspend for 2 sec.')
                time.sleep(2)
            elif self.cur_page == 'network_err':
                adb.click_btn(self.serial, 'retry.png')
            elif self.cur_page == 'select':
                adb.click_btn(self.serial, 'select.png')
            elif self.cur_page == 'prepare':
                adb.click_btn(self.serial, 'start.png')
            elif self.cur_page == 'again':
                adb.click_btn(self.serial, 'again.png')
            elif self.cur_page == 'okpop':
                adb.click_btn(self.serial, 'ok.png')
            elif self.cur_page == 'closepop':
                adb.click_btn(self.serial, 'close.png')
            elif self.cur_page == 'dl':
                adb.click_btn(self.serial, 'download.png')
            elif self.cur_page == 'bingo':
                adb.click_btn(self.serial, 'pok.png')
            elif self.cur_page == 'live':
                time.sleep(4)
            elif self.cur_page == 'network_err':
                print('Network Error. Retry after 5 sec')
                adb.click_btn(self.serial, 'retry.png')
                time.sleep(4)
