import cv2
import os, time

page_route = 'template\\ui\\pages'


def match(target: str, template: str):
    print(template)
    target = cv2.imread(target)
    template = cv2.imread(template)
    t_height, t_width = template.shape[:2]
    result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
    cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val)
    flag = (abs(min_val) <= 1e-10)
    return {
        "flag": flag,
        "min_loc": min_loc,
        "max_loc": max_loc,
        "height": t_height,
        "width": t_width
    }


def is_page(target: str, page_name: str) -> bool:
    if page_name == 'other':
        return True
    else:
        if not os.path.exists(os.path.join(page_route, page_name)):
            return False
        for tp in os.listdir(os.path.join(page_route, page_name)):
            if not match(target, os.path.join(page_route, page_name, tp))['flag']:
                return False
    return True
