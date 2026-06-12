import numpy as np
import matplotlib.pyplot as plt
from masking import HSV_BOUNDS

def calculate_stats(masks, y1, y2, x1, x2, ppmm2):
        rect_disease  = masks["final"][y1:y2, x1:x2]
        rect_brown = masks["brown"][y1:y2, x1:x2]
        rect_yellow= masks["yellow"][y1:y2, x1:x2]
        rect_green = masks["green"][y1:y2, x1:x2]

        disease_px   = int(np.count_nonzero(rect_disease))
        brown_px= int(np.count_nonzero(rect_brown))
        yellow_px=int(np.count_nonzero(rect_yellow))
        leaf_px   = int(np.count_nonzero(rect_green))
        pct       = (disease_px / leaf_px * 100) if leaf_px > 0 else 0.0

        disease_mm2 = round(disease_px / ppmm2[0], 4)
        brown_mm2 = round(brown_px / ppmm2[0], 4)
        yellow_mm2 = round(yellow_px / ppmm2[0], 4)
        return disease_mm2,brown_mm2,yellow_mm2
def plot_hsv_histogram(img_hsv, y1, y2, x1, x2):
    rectangle_hsv = img_hsv[y1:y2, x1:x2]
    
    hue        = rectangle_hsv[:, :, 0].ravel()  # 0-180
    saturation = rectangle_hsv[:, :, 1].ravel()  # 0-255
    value      = rectangle_hsv[:, :, 2].ravel()  # 0-255

    b = HSV_BOUNDS
    fig_hist, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig_hist.suptitle(f"HSV Distribution for Rectangle Area ({x1},{y1})→({x2},{y2})")

    # Hue
    axes[0].hist(hue, bins=180, range=(0, 180), color="red", alpha=0.7)
    axes[0].set_title("Hue (0-180)")
    axes[0].set_xlabel("Hue value")
    axes[0].set_ylabel("Pixel count")

    # Draw your current hue bounds as vertical lines
    axes[0].axvline(x=b["light_yellow"][0][0],   color="blue",  linestyle="--", label="lower red")
    axes[0].axvline(x=b["light_yellow"][1][0],   color="blue",  linestyle="-",  label="upper red")
    axes[0].axvline(x=b["light_brown"][0][0], color="brown", linestyle="--", label="lower light brown")
    axes[0].axvline(x=b["light_brown"][1][0], color="brown", linestyle="-",  label="upper light brown")
    axes[0].axvline(x=b["dark_brown"][0][0], color="brown", linestyle="--", label="lower dark brown")
    axes[0].axvline(x=b["dark_brown"][1][0], color="brown", linestyle="-",  label="upper dark brown")
    axes[0].legend(fontsize=7)

    # Saturation
    axes[1].hist(saturation, bins=255, range=(0, 255), color="green", alpha=0.7)
    axes[1].set_title("Saturation (0-255)")
    axes[1].set_xlabel("Saturation value")
    axes[1].axvline(x=b["light_brown"][0][1], color="brown", linestyle="--", label="lower bound")
    axes[1].axvline(x=b["light_brown"][1][1], color="brown", linestyle="-",  label="upper bound")
    axes[1].legend(fontsize=7)

    # Value
    axes[2].hist(value, bins=255, range=(0, 255), color="blue", alpha=0.7)
    axes[2].set_title("Value/Brightness (0-255)")
    axes[2].set_xlabel("Value")
    axes[2].axvline(x=b["light_brown"][0][2], color="brown", linestyle="--", label="lower bound")
    axes[2].axvline(x=b["light_brown"][1][2], color="brown", linestyle="-",  label="upper bound")
    axes[2].legend(fontsize=7)

    plt.tight_layout()
    plt.show()
