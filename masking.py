import cv2 as cv

DISH_DIAMETER_MM = 90

HSV_BOUNDS = {
    "darkest_brown": ((170,  10, 90), (179, 255, 255)),
    "dark_brown":   ((0,  10, 90), (18, 255, 255)),
    "light_brown":  ((18, 10, 90), (27, 255, 245)),
    "light_yellow": ((28, 55, 90), (32, 255, 225)),
    "dark_yellow":  ((33,110, 90), (36, 255, 200)),
    "green":        ((35, 10,  10), (85, 255, 255)),
}

OVERLAY_COLORS = {
    "darkest_brown":  [139,  69,  19],
    "dark_brown":  [139,  69,  19],
    "light_brown": [196, 164, 132],
    "light_yellow":      [255, 255,   0],
    "dark_yellow": [255, 255,   0],
}
def make_masks(img_hsv):
    b = HSV_BOUNDS
    masks = {k: cv.inRange(img_hsv, *v) for k, v in b.items()}
    masks["brown"]  = masks["dark_brown"]  + masks["light_brown"] + masks["darkest_brown"]
    masks["yellow"] = masks["light_yellow"]      + masks["dark_yellow"]
    masks["final"]  = masks["brown"]       + masks["yellow"]
    return masks

def make_overlay(img_rgb, masks):
    overlay = img_rgb.copy()
    for key, color in OVERLAY_COLORS.items():
        overlay[masks[key] == 255] = color
    overlay[masks["final"] == 0] = [0, 0, 0]
    return cv.addWeighted(img_rgb, 0.2, overlay, 0.8, 0)