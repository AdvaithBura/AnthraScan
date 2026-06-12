import cv2 as cv
import matplotlib.pyplot as plt
import sys
from file_handler import image_name_extraction
from masking import make_masks, make_overlay
from handlers import make_handlers

image_source= r"example.JPG"

#Image initialization
image_path = sys.argv[1] if len(sys.argv) > 1 else image_source
img = cv.imread(image_path)
if img is None:
    raise FileNotFoundError(f"Could not load image: {image_path}")

#Creating rgb and hsv versions of image
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img_hsv=cv.cvtColor(img, cv.COLOR_BGR2HSV)

csv_filename,filename, name, day, plate1, plate2, two_plates = image_name_extraction(image_path)
masks=make_masks(img_hsv)

blended = make_overlay(img_rgb,masks) #makes it so the paint layer is semitransparent(to see actual image)

#Display
fig, (ax_orig, ax_result) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle(filename+"\nClick and drag on the LEFT panel to measure petri dish radius", fontsize=15)

ax_orig.imshow(img_rgb)
ax_orig.set_title("Original")
ax_result.imshow(blended)
ax_result.set_title("Disease detection: draw rectangle over diseased area")

onclick, on_motion, on_release, on_key=make_handlers(ax_result,fig,ax_orig,masks,name,day,plate1,plate2,filename,two_plates,img_hsv,csv_filename)

#Activating user input functions
fig.canvas.mpl_connect("button_press_event",  onclick)
fig.canvas.mpl_connect("motion_notify_event", on_motion)
fig.canvas.mpl_connect("button_release_event", on_release)
fig.canvas.mpl_connect("key_press_event", on_key)

plt.tight_layout()
plt.show()