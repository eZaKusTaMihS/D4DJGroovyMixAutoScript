import os, time
from adb_control import AdbController
from img_process import ImgProcessor

page_route = 'template\\ui\\page'
m_lim = 1e-9
adb = AdbController(serial='127.0.0.1:16416')
ip = ImgProcessor()


class D4Controller:
    screen = None
    serial = '127.0.0.1:16416'
    pages = ['okpop', 'closepop', 'next', 'bingo', 'select', 'prepare', 'again', 'livein', 'main', 'title', 'live']
    cur_page = 'none'
    last_page = 'none'
    voltage = 0
    event_pt = 0

    def __init__(self, serial='127.0.0.1:16416'):
        self.serial = serial

    def start(self):
        dt = 0
        while True:
            ct = time.time()
            self.__update_stat(optimize=False)
            if self.cur_page != self.last_page:
                print('current status: %s' % self.cur_page)
            self.__react_page(self.cur_page)
            if self.cur_page == 'prepare' and self.last_page == 'select':
                print('Loop time cost: %.2fs' % dt)
                dt = 0
            else:
                dt += (time.time() - ct)
            # time.sleep(np.random.random() / 2 + 0.5)

    def get_stat(self) -> dict:
        self.__update_stat()
        return {
            "cur_page": self.cur_page,
            "voltage": self.voltage,
            "event_pt": self.event_pt
        }

    def __get_screen(self) -> str:
        sc_path = os.path.join(os.getcwd(), 'temp\\cur_screen.png')
        adb.screenshot(sc_path)
        return sc_path

    def __update_stat(self, optimize: bool = True) -> None:
        self.__update_page(optimize)

    def __update_page(self, optimize: bool = True) -> None:
        self.screen = self.__get_screen()
        self.last_page = self.cur_page
        if optimize:
            if self.__update_page_opt():
                return
        min_val = 100
        min_page = 'none'
        for page_name in self.pages:
            p_path = os.path.join(page_route, page_name)
            if not os.path.exists(p_path):
                continue
            cnt, min_v = 0, 0
            for i in os.listdir(p_path):
                cnt += 1
                min_v += ip.match(self.screen, os.path.join(p_path, i))['min_val']
            min_v /= cnt
            if min_v < m_lim and min_v < min_val:
                min_val = min_v
                min_page = page_name
        self.cur_page = min_page
        return

    def __update_page_opt(self) -> bool:
        """
        Update with some optimized match to avoid matching all templates for all possible pages.
        :return: Whether optimized match succeeds.
        """
        flag = False
        cur_page = 'none'
        match self.last_page:
            case 'again':
                cur_page = 'select'
                if ip.matches_page(self.screen, cur_page):
                    if not ip.matches(self.screen, 'template\\content\\select\\cateye.png'):
                        adb.click_btn('cateye')
                    adb.click_btn('decide')
                    time.sleep(0.5)
            case 'select':
                cur_page = 'prepare'
                if ip.matches_page(self.screen, cur_page):
                    flag = adb.click_btn('start')
        if flag:
            self.cur_page = cur_page
        return flag

    def __react_page(self, page: str):
        # Handle Unexpected situations
        if page == 'loading':
            time.sleep(1)
            return
        if page == 'network_err':
            print('Network Error.')
            time.sleep(4)
            return
        if page == 'closepop':
            if not adb.click_btn('close.png'):
                adb.click_btn('ok.png', do_screenshot=False)
            return
        if page == 'okpop':
            if not adb.click_btn('ok.png'):
                adb.click_btn('close.png', do_screenshot=False)
            return
        # Handle normal pages
        if page == 'title':
            adb.click((640, 360), 0, 0)
        if page == 'select':
            if not ip.matches(self.screen, 'template\\content\\select\\cateye.png'):
                adb.click_btn('cateye.png')
            adb.click_btn('decide.png')
            time.sleep(0.5)
            return
        if page == 'main':
            adb.click_btn('golive.png')
            return
        if page == 'next':
            adb.click_btn('next.png')
            time.sleep(1)
            return
        if page == 'prepare':
            adb.click_btn('start.png')
            return
        if page == 'again':
            adb.click_btn( 'again.png')
            time.sleep(1.5)
            return
        if page == 'bingo':
            adb.click_btn('pok.png')
            return
        if page == 'livein':
            adb.click_btn('livein.png')
            return
        if page == 'live':
            time.sleep(2)
            return
        # Handle default situation
        if adb.click_btn('close.png'):
            print('close')
            return
        if adb.click_btn('ok.png', do_screenshot=False):
            print('ok')
            return
        if adb.click_btn('next.png'):
            print('next')
            return
        if adb.click_btn('pok.png', do_screenshot=False):
            print('pok')
            return
