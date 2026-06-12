This Image Analysis Program is able to detect preset color ranges within images. This project was primarily designed for biological use, especially for detcting lesion sizes of sorghum anthracnose in a cut leaf assay on a petri dish. Much of the functionality is designed around this but it can be utilized for various other factors. 

Python 3.8 or higher is recommended.
Install dependencies with:
```
pip install opencv-python numpy matplotlib
```

```
Sorghum Project Image Analysis Program/
├── Main.py
├── masking.py
├── handlers.py
├── analysis.py
└── file_handler.py
```

Running the program:
To run the program, pass the following as a command line argument:
```bash
    python Main.py "path/to/your/image.jpg"
```

If no argument is given, the program will fall back to a default image path defined in Main.py in the image_source variable. A sample demo can be run with the default image to test program features. The program will output a csv file in the following format: 

```csv
    name,day,disease mm2,light infection mm2,dark infection mm2,Scale (px/mm2)
    G2 BTX623,6,0.4021,0.4021,0.0,771.01
```

Inputs in the code:
1. Image file path- Refer to "Running the program" above

2. Color detection- In masking.py there are some present color ranges present in HSV_BOUNDS in hsv values. You can add your own HSV values to detect a specific color. The mask is created in masking.py under the make_masks function. Update 
masks["final"] for the proper mask to be displayed. The program has functionality to assist in determining optimal color ranges. Check 3c under functionality.

3. Overlay color(optional)- In masking.py there are some preset colors in OVERLAY_COLORS. This will paint the colors you want to detect from HSV_BOUNDS the specified color. Make sure the color name matches in both HSV_BOUNDS and OVERLAY_COLORS

4. DISH_DIAMETER_MM- In masking.py. Reminder that this was designed in a biological perspective and was designed for petri dishes. To convert pixels to mm, this conversion factor is used. While designed to get a conversion factor from circular objects, linear objects are also usable as the diameter is merely the length of one side of the circle to the other side. As such it can be treated as a line. This conversion factor can be used on any reference object. Make sure to preset this value.


The program is user friendly and prompts user to do specific actions via a title text on the figure at the top
Functionality:
1. Figure- The program will create a figure using matplotlib. This figure will feature the original image on the left and the image containing the mask on the right. The mask will mostly show only the masks but it will also have a faint background of the original image in the background

2. Interactive Images- The images allow you to click and drag on them to analyze them properly. Continue reading to learn the possiblities of these interactions.

3. Setting Reference- On the image on the left, click and drag mouse from one end of reference object to other end of reference object. Remember to set DISH_DIAMETER_MM to proper value prior to setting the conversion factor. The conversion factor can be seen on top of the image once drawn. If the reference drawn is not satisfactory you may redraw the reference BEFORE doing anything on the right image

4. Mask Analysis- The image on the right allows you to draw a box over any area by clicking and dragging. Once done, it is in a pending state and there are multiple options present to you. 
    a. First, if the image name contains the word "and" or the symbol "+" it will attempt to separate the image name into the two file names. This feature is useful in the biological setting where images often contained two petri dishes with different experimental conditions. If you would like to keep the full name for the csv file, type "3", otherwise type "1" or "2" based on the desired name that the code should save the data point under in the csv. A prompt will be present above the image to guide you through this process.
    b. Next, you can only do one of these options. Desiring to choose a new option requires you to draw a new box:
        i. Type the letter "y": This will confirm the box, allowing you to see the area of the mask and will also save the data into the csv file. This box will determine the amount of the specified mask within the box in units of mm2 or whatever your conversion factor unit is. This cannot be undone through the code so ensure you are satisfied with the box before typing "y".
        ii. Type the letter "n": This will discard the box. Use only if you are not satisfied with the box drawn.
        iii. Type the letter "m": This will create a histogram of all the HSV values within the given box. This feature is very helpful when handling a new image and you are unsure of the appropriate HSV values for the mask, aiding in determining accurate HSV ranges for the mask. Typing "m" will not save the box and a new box will need to be drawn to save the box data into the csv file.

5. CSV file Data Saving- The program will automatically save the details of each data point you add. This data point is determined by 4a. i. directly above. The csv file created will be named the folder of the image file being analyzed. It will contain a couple metrics, including: name, day, disease_mm2, light_infection_mm2, dark_infection_mm2, Scale (px/mm2)
***To remove or add or modify any of this inputs, go to the pending_entry dictionary in the on_release function in the handlers.py file.
    a. name: The name of the file. If the word day is present it will strip it out.
    b. day: A number indicating the day that image was taken. Will take the number after the word day.
    c. disease_mm2: Area of the mask in the drawn box (in current code area of mask["final"])
    d. light_infection_mm2: Area of another mask in drawn box (in current code area of mask["yellow"])
    e. dark_infection_mm2: Area of another mask in the drawn box (in current code area of mask["brown"])
    f. Scale (px/mm2): The conversion factor between pixels and mm2

Thank you for reading and learning this program. I hope this program is helpful to whatever your ventures are!