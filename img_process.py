import cv2
import easyocr

# reader = easyocr.Reader(['jp', 'en'])
page_route = 'template\\ui\\page'
m_lim = 1e-9


def match(target: str, template: str) -> dict:
    target = cv2.imread(target)
    template = cv2.imread(template)
    t_height, t_width = template.shape[:2]
    result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
    cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return {
        "min_val": abs(min_val),
        "min_loc": min_loc,
        "max_loc": max_loc,
        "height": t_height,
        "width": t_width
    }


def matches(target: str, template: str, lim: float = m_lim) -> bool:
    return matches_dt(match(target, template), lim)


def matches_dt(btn_data: dict, lim: float = m_lim) -> bool:
    return btn_data['min_val'] <= lim
