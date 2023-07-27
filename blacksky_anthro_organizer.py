import os
import shutil
from tkinter import filedialog as fd
import tkinter as tk
import json

# Get rid of tkinter root window
root = tk.Tk()
root.withdraw()

# Ask which folder needs to be processed
directoryname = fd.askdirectory()
os.chdir(directoryname)

# Initialize lists used to store the unique dates and catelog IDs encountered
dates = []
imageIDs = []
years = []

with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.is_dir():
            os.chdir(file)
            with os.scandir(os.getcwd()) as directory2:
                for file2 in directory2:

                    # Standard product
                    if file2.name.startswith('BSG-1'):
                        imageID = file2.name[24:33]
                        date = file2.name[8:12]+'_'+file2.name[12:14]+'_'+file2.name[14:16]
                        if date not in dates:
                            os.mkdir(date)
                            dates.append(date)
                            shutil.move(date, directoryname)
                        if imageID not in imageIDs:
                            os.mkdir(imageID)
                            imageIDs.append(imageID)
                            shutil.move(imageID, directoryname+'/'+date)
                            os.mkdir('Anthro')
                            shutil.move('Anthro', directoryname+'/'+date+'/'+imageID)
                        shutil.move(file2, directoryname+'/'+date+'/'+imageID+'/Anthro')
                    
                    # Area Coverage product
                    if file2.name.startswith('BSG-AREA'):
                        imageID = file2.name[29:37]+'_AREA'
                        date = file2.name[13:17]+'_'+file2.name[17:19]+'_'+file2.name[19:21]
                        if date not in dates:
                            os.mkdir(date)
                            dates.append(date)
                            shutil.move(date, directoryname)
                        if imageID not in imageIDs:
                            os.mkdir(imageID)
                            imageIDs.append(imageID)
                            shutil.move(imageID, directoryname+'/'+date)
                            os.mkdir('Anthro')
                            shutil.move('Anthro', directoryname+'/'+date+'/'+imageID)
                        shutil.move(file2, directoryname+'/'+date+'/'+imageID+'/Anthro')

                os.chdir('..')

# Delete the old folder
with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.name.startswith('BSG'):
            shutil.rmtree(file.name)

# Move the date folders into year folders
with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.is_dir():
            year = file.name[0:4]
            if year not in years:
                os.mkdir(year)
                years.append(year)
            shutil.move(file, year)

print('Dates:')
print(dates)
print('Image IDs:')
print(imageIDs)
