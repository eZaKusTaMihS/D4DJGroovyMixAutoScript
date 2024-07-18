import cv2
import os
import easyocr


class ImgProcessor:
    __screen = 'temp\\cur_screen.png'
    __page_route = 'template\\ui\\page'
    __lim = 1e-9

    def __init__(self, page_route: str = 'template\\ui\\page', lim: float = 1e-9) -> None:
        self._page_route = page_route
        self.__lim = lim
        # self.__text_reader = easyocr.Reader(['en'])
        return

    def match(self, target: str, template: str) -> dict:
        try:
            target = cv2.imread(target)
            template = cv2.imread(template)
            t_height, t_width = template.shape[:2]
            result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
            cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        except:
            print('Error occurred during matching %s and %s. Please check whether file path is available.' % (target, template))
            min_val, min_loc, t_height, t_width = 100, (0, 0), 0, 0
        return {
            "min_val": abs(min_val),
            "min_loc": min_loc,
            "height": t_height,
            "width": t_width
        }

    def matches(self, target: str, template: str, lim: float = __lim) -> bool:
        return self.matches_dt(self.match(target, template), lim)

    def matches_dt(self, btn_data: dict, lim: float = __lim) -> bool:
        return btn_data['min_val'] < lim

    def matches_page(self, target: str, page_name: str, lim: float = __lim) -> bool:
        return self.__match_page(target, page_name) < lim

    def __match_page(self, target: str, page_name: str) -> float:
        page_folder = os.path.join(self.__page_route, page_name)
        if os.path.isdir(page_folder):
            cnt = 0
            min_val = 0
            for file in os.listdir(page_folder):
                cnt += 1
                template = os.path.join(page_folder, file)
                min_val += self.match(target, template)['min_val']
            min_val /= cnt
            return min_val
        return 100
