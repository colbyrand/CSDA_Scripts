import os
import shutil
from tkinter import filedialog as fd
import tkinter as tk

# Get rid of tkinter root window
root = tk.Tk()
root.withdraw()

# Create folders to store drone files
directoryname = fd.askdirectory()
os.chdir(directoryname)
os.mkdir('Photography')
os.mkdir('Drone_GNSS')
os.mkdir('Survey_Imagery')
os.chdir('Survey_Imagery')
os.mkdir('RGB')
os.mkdir('Green')
os.mkdir('Red')
os.mkdir('Red_Edge')
os.mkdir('NIR')
os.chdir('..')

# Create array to store photography image IDs
photography_image_ID = []

with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.is_dir() and not file.name == 'Survey_Imagery' and not file.name == 'Photography' and not file.name == 'Drone_GNSS':
            os.chdir(file.name)
            with os.scandir(os.getcwd()) as directory2:
                for file2 in directory2:
                    if file2.name.endswith('D.JPG'):
                        shutil.move(file2, directoryname+'/Survey_Imagery/RGB')
                    elif file2.name.endswith('F.JPG'):
                        shutil.move(file2, directoryname+'/Photography')
                        photography_image_ID.append(file2.name.split('_')[0:2])     # add this image ID to the array
                    elif file2.name.endswith('G.TIF'):
                        shutil.move(file2, directoryname+'/Survey_Imagery/Green')
                    elif file2.name.endswith('_R.TIF'):
                        shutil.move(file2, directoryname+'/Survey_Imagery/Red')
                    elif file2.name.endswith('RE.TIF'):
                        shutil.move(file2, directoryname+'/Survey_Imagery/Red_Edge')
                    elif file2.name.endswith('NIR.TIF'):
                        shutil.move(file2, directoryname+'/Survey_Imagery/NIR')
                    elif file2.name.endswith('.nav'):
                        shutil.move(file2, directoryname+'/Drone_GNSS')
                    elif file2.name.endswith('.obs'):
                        shutil.move(file2, directoryname+'/Drone_GNSS')
                    elif file2.name.endswith('.bin'):
                        shutil.move(file2, directoryname+'/Drone_GNSS')
                    elif file2.name.endswith('.MRK'):
                        shutil.move(file2, directoryname+'/Drone_GNSS')
            os.chdir('..')

os.chdir('Survey_Imagery')
with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.is_dir():
            os.chdir(file.name)
            with os.scandir(os.getcwd()) as directory2:
                for file2 in directory2:
                    if file2.name.split('_')[0:2] in photography_image_ID:
                        shutil.move(file2, directoryname+'/Photography')
            os.chdir('..')