import re, os, csv
from pathlib import Path

def image_name_extraction(image_path):
    path=Path(image_path)
    csv_filename=path.parent.name

    #Splitting file name into trial name and day number
    file = os.path.basename(image_path)
    filename = os.path.splitext(file)[0]
    name_split=filename.find("day")
    name=None
    if name_split ==-1:
        name_split=filename.find("Day")
    if name_split ==-1:
        name_split=None
        name=filename
        day=None
    else: 
        name= filename[:name_split]
        day= filename[name_split+3:]
        day= re.sub(r"\D", "", day)

    two_plates=True
    plate1=None
    plate2=None
    split_name=name.replace("and","+")
    plate_split=split_name.find("+")
    if plate_split==-1:
        two_plates=False
        name=re.sub(r'\A[^.\w]+|[._]+\Z', "", name)
    else:
        plate1=split_name[:plate_split]
        plate1=re.sub(r'\A[_|\W]+|[_|\W]+\Z', "", plate1)
        plate2=split_name[plate_split+1:]
        plate2=re.sub(r'\A[_|\W]+|[_|\W]+\Z', "", plate2)
    
    return csv_filename, filename, name, day, plate1, plate2, two_plates

def log_to_csv(csv_filename,results_log):
    if not results_log:
        return

    #Opens/making a csv file names infection_results.csv
    os.makedirs("Infection_Results", exist_ok=True)
    filepath = os.path.join("Infection_Results", csv_filename + ".csv")

    file_exists = os.path.exists(filepath)

    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results_log[0].keys())
        
        if not file_exists:
            writer.writeheader()  # only write header if file is new
        else:
            #If file already exists, ensures it is not empty, if it is, it will write the header
            with open(filepath, "r") as read_f:
                first_line=read_f.readline().strip()
                if not first_line:
                    writer.writeheader() #write header if file is empty but csv file already exists

        
        writer.writerow(results_log[-1])  # only write the latest entry