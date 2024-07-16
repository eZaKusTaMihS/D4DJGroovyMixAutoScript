import os, time
import recog
import adb_control as adb


def get_screen() -> str:
    sc_path = os.path.join(os.getcwd(), 'temp\\cur_screen.png')
    adb.get_cur_screen('16416', sc_path)
    return sc_path


class D4Controller:
    serial = '16416'
    pages = ['fin', 'network_err', 'loading', 'select', 'prepare', 'play', 'fin', 'again', 'okpop', 'closepop', 'dl']
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

    def update_stat(self):
        screen = get_screen()
        for page_name in self.pages:
            if recog.is_page(screen, page_name):
                self.cur_page = page_name
                break
        pass

    def start(self):
        while True:
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
            else:
                time.sleep(2)
