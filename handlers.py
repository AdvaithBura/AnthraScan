# handlers.py
import numpy as np
import matplotlib.patches as mpatches
from analysis import calculate_stats, plot_hsv_histogram
from file_handler import log_to_csv
from masking import DISH_DIAMETER_MM

def make_handlers(ax_result,fig,ax_orig,masks,name,day,plate1,plate2,filename,two_plates,img_hsv,csv_filename):
    clicked=[None]

    #Rectangle variable initialization
    coords      = []
    current_rect = [None]
    bg_cache=[None] 

    #Results storage variable initialization
    results_log = []
    pending_entry = [None]

    #Circle variable initialization(to determine petri dish size)
    dish_circle_coords = []
    current_circle = [None]
    bg_cache_orig = [None]


    #Variable for conversion factor for pixels to mm
    ppmm2=[None]
    def onclick(event):
        # RIGHT panel for disease area selection
        if event.inaxes == ax_result:
            #Ensures click only occurs in image bounds
            if event.xdata is None or event.ydata is None:
                return
            if ppmm2[0] is None:
                return
            coords.clear()
            coords.append((int(event.xdata), int(event.ydata))) #records (x,y) of clicked spot
            bg_cache[0] = fig.canvas.copy_from_bbox(ax_result.bbox)
        # LEFT panel for petri dish area initialization
        elif event.inaxes == ax_orig:
            if event.xdata is None or event.ydata is None:
                return
            dish_circle_coords.clear()
            dish_circle_coords.append((int(event.xdata), int(event.ydata)))
            bg_cache_orig[0] = fig.canvas.copy_from_bbox(ax_orig.bbox) #Records and remembers original image
    
    def on_motion(event):
        #Rectangle drawing
        if event.inaxes == ax_result:
            if len(coords)==0:
                return
            if event.xdata is None or event.ydata is None:
                return
            if bg_cache[0] is None:
                return
            
            #Rectangle parameters
            x1, y1 = coords[0]
            x2, y2 = int(event.xdata), int(event.ydata)

            fig.canvas.restore_region(bg_cache[0]) #Clears old rectangle frame by restoring original background
            #Creates the rectangle if not already there or updates the x,y value if it is already present
            if current_rect[0] is None:
                rect = mpatches.Rectangle(
                    (min(x1, x2), min(y1, y2)), abs(x2 - x1), abs(y2 - y1),
                    linewidth=1.5, edgecolor="white", facecolor="none", linestyle="--"
                )
                current_rect[0] = ax_result.add_patch(rect)
            else:
                current_rect[0].set_xy((min(x1, x2), min(y1, y2)))
                current_rect[0].set_width(abs(x2 - x1))
                current_rect[0].set_height(abs(y2 - y1))

            #Draws rectangle on screen
            ax_result.draw_artist(current_rect[0])
            fig.canvas.blit(ax_result.bbox)

        #Circle drawing
        elif event.inaxes == ax_orig:
            if not dish_circle_coords or event.xdata is None or event.ydata is None:
                return
            if bg_cache_orig[0] is None:
                return

            #Circle parameters
            cx, cy = dish_circle_coords[0]
            ex, ey = int(event.xdata), int(event.ydata)
            radius = np.sqrt((ex - cx)**2 + (ey - cy)**2)/2

            fig.canvas.restore_region(bg_cache_orig[0]) #Clears old rectangle frame by restoring original background

            #Creates the circle if not already there or updates the center and radius value if it is already present
            if current_circle[0] is None:
                circle = mpatches.Circle(
                    ((cx+ex)/2, (cy+ey)/2), radius,
                    linewidth=1.5, edgecolor="yellow", facecolor="none", linestyle="--"
                )
                current_circle[0] = ax_orig.add_patch(circle)
            else:
                current_circle[0].center = ((cx+ex)/2, (cy+ey)/2)
                current_circle[0].radius = radius

            #Draws the rectangle
            ax_orig.draw_artist(current_circle[0])
            fig.canvas.blit(ax_orig.bbox)
    
    def on_release(event):
        #Rectangle
        if event.inaxes == ax_result:
            if event.xdata is None or event.ydata is None:
                return
            if len(coords) == 0:
                return

            #Obtains final rectangle x,y coordinates
            coords.append((int(event.xdata), int(event.ydata)))
            (x1, y1), (x2, y2) = coords
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))

            #Remove the old rectangle
            if current_rect[0] is not None:
                current_rect[0].remove()
                current_rect[0] = None

            # Draw final rectangle
            rect = mpatches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=2, edgecolor="yellow", facecolor="none"  # yellow = pending
            )
            current_rect[0] = ax_result.add_patch(rect)

            # Calculate stats
            disease_mm2,brown_mm2,yellow_mm2=calculate_stats(masks, y1, y2, x1, x2, ppmm2)


            # Store the vital values in a dictionary in a pending status(needs to be confirmed by user first if rectangle is correct)
            pending_entry[0] = {
                "rect":           current_rect[0],
                "name":          name,
                "day":            day,
                "disease mm2":    disease_mm2,
                "light infection mm2": yellow_mm2,
                "dark infection mm2":brown_mm2,
                "Scale (px/mm2)": round(ppmm2[0],2),
                "x1": x1, 
                "y1": y1,
                "x2": x2,
                "y2": y2
            }
            if two_plates==True:
                ax_result.set_title("Two names found. If error: click 3. \nClick 1 if plate is "+plate1+" Click 2 if plate is "+plate2, color="black")
                fig.canvas.draw_idle()
            else:
                print(f"Keep this rectangle? Press Y to save, N to discard")
                ax_result.set_title("Keep this rectangle? Press Y to save, N to discard", color="red")

            fig.canvas.draw_idle() # Draws the changes
            coords.clear() #Clears the coords var so a new rectangle can be drawn

        #Circle
        elif event.inaxes == ax_orig:
            if not dish_circle_coords or event.xdata is None or event.ydata is None:
                return

            #Obtain final circle details
            cx, cy = dish_circle_coords[0]
            ex, ey = int(event.xdata), int(event.ydata)
            pixel_diameter = np.sqrt((ex - cx)**2 + (ey - cy)**2)

            # Remove dashed preview circle, draw solid final circle
            if current_circle[0] is not None:
                current_circle[0].remove()
                current_circle[0] = None

            circle = mpatches.Circle(
                ((cx+ex)/2, (cy+ey)/2), pixel_diameter/2,
                linewidth=2, edgecolor="cyan", facecolor="none", linestyle="-"
            )
            ax_orig.add_patch(circle)
            current_circle[0]=circle

            # Calculate and store scale
            pixels_per_mm = pixel_diameter / DISH_DIAMETER_MM
            ppmm2[0] = pixels_per_mm **2
            print(f"Dish diameter: {pixel_diameter:.1f}px = {DISH_DIAMETER_MM}mm")
            print(f"Scale: {pixels_per_mm:.2f} px/mm")
            ax_orig.set_title(f"Scale set: {pixels_per_mm:.1f} px/mm", color="magenta")

            fig.suptitle(filename+"\nClick and drag on the RIGHT panel to detect diseased area", fontsize=15)

            dish_circle_coords.clear()
            fig.canvas.draw_idle()

    def on_key(event):

        #Ensures rectangle is drawn first
        if pending_entry[0] is None:
            return
        
        entry = pending_entry[0]

        if two_plates==True and clicked[0] is None:
            if event.key=="1":
                entry["name"]=plate1
                ax_result.set_title("Keep this rectangle? Press Y to save, N to discard", color="red")
                print("Sample name: "+ entry["name"])
                fig.canvas.draw_idle()
                clicked[0]=True
            elif event.key=="2":
                entry["name"]=plate2
                ax_result.set_title("Keep this rectangle? Press Y to save, N to discard", color="red")
                print("Sample name: "+ entry["name"])
                fig.canvas.draw_idle()
                clicked[0]=True
            elif event.key=="3":
                ax_result.set_title("Keep this rectangle? Press Y to save, N to discard", color="red")
                print("Sample name: "+ entry["name"])
                fig.canvas.draw_idle()
                clicked[0]=True
            return
        
        #If user presses y, saves data point
        if event.key == "y":
            # Draw final rectangle
            rect = mpatches.Rectangle(
                (entry["x1"], entry["y1"]), entry["x2"] - entry["x1"], entry["y2"] - entry["y1"],
                linewidth=2, edgecolor="cyan", facecolor="none"
            )
            ax_result.add_patch(rect)

            # Annotate 
            ax_result.text(
                entry["x1"], entry["y1"] - 10, f"{entry['disease mm2']} mm2 disease",
                color="cyan", fontsize=9, fontweight="bold",
                bbox=dict(facecolor="black", alpha=0.5, pad=2)
            )

            # Save to log
            log_data = {k: v for k, v in entry.items() 
                        if k not in ("rect", "x1", "y1","x2","y2")}  # ignore unwanted fields
            results_log.append(log_data)
            log_to_csv(csv_filename,results_log)
            print("Saved.")
            clicked[0]=None
            ax_result.set_title("Disease detection: draw rectangle over diseased area", color="black")

        #If user wishes to discard the rectangle
        elif event.key == "n":
            # Remove rectangle and discard
            pending_entry[0]["rect"].remove()
            current_rect[0]=None
            print("Discarded.")
            clicked[0]=None

            ax_result.set_title("Disease detection: draw rectangle over diseased area",color="black")
        elif event.key == "m":
            plot_hsv_histogram(img_hsv, entry["y1"], entry["y2"], entry["x1"], entry["x2"])
            print("Plotted")
            clicked[0]=None

            ax_result.set_title("Disease detection: draw rectangle over diseased area",color="black")


        pending_entry[0] = None
        fig.canvas.draw_idle()
    return onclick, on_motion,on_release, on_key