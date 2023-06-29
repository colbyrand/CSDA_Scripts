##################################################################################
#                           Planet Downloads Organizer

# Written by Colby Rand
# 2023/06/29

# This script takes PlanetScope imagery downloaded through Planet Explorer and organizes
# them in the following hierarchy: sensor -> date -> image ID -> all files. Before
# running this script, make sure all downloaded folders are located in a single
# folder. Run the script by calling python from the terminal and then selecting the
# folder with the imagery that needs processing:

# python planet_downloads_organizer.py

##################################################################################

import os
from tkinter import filedialog as fd
import tkinter as tk
import shutil
from zipfile import ZipFile
import json

# Get rid of tkinter root window
root = tk.Tk()
root.withdraw()

# Ask which folder needs to be processed
directoryname = fd.askdirectory()
os.chdir(directoryname)

# Initialize lists used to store the unique dates and catelog IDs encountered
PlanetScope_dates = []
PlanetScope_IDs = []
planetscope_present = 0     # variables to indicate if PlanetScope images were encountered
zip_present = 0

# Check if compressed files are present
with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.name.endswith('.zip'):
            zip_present = 1

# Uncompress all the zip files
if zip_present == 1:
    with os.scandir(os.getcwd()) as directory:
        for file in directory:
            if file.name.endswith('.zip'):
                print('Extracting: ' + file.name + '...')
                with ZipFile(os.getcwd()+'/'+file.name, 'r') as f:
                    f.extractall('unzip')

    os.chdir('unzip')
    with os.scandir(os.getcwd()) as directory:
        for file in directory:
            if file.name.endswith('MACOSX') == False and file.is_dir:
                shutil.move(file, directoryname)

    os.chdir('..')
    with os.scandir(os.getcwd()) as directory:
        for file in directory:
            if file.name.endswith('.zip'):
                os.remove(file)
            if file.name.endswith('unzip'):
                shutil.rmtree(file)

# Move image folders to PlanetScope folder
with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.is_dir():
            if 'psscene' in file.name:
                if planetscope_present == 0:
                    os.mkdir('PlanetScope')
                planetscope_present = 1
                shutil.move(file, 'PlanetScope')

# Organize PlanetScope folders
with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.name == 'PlanetScope':
            os.chdir('PlanetScope')         # enter PlanetScope folder
            with os.scandir(os.getcwd()) as directory2:
                for file2 in directory2:
                    if file2.is_dir:
                        os.chdir(file2.name)    # enter image folder
                        with os.scandir(os.getcwd()) as directory3:
                            for file3 in directory3:
                                if file3.name == 'PSScene':
                                    os.chdir(file3)     # enter PSScene folder
                                    with os.scandir(os.getcwd()) as directory4:
                                        for file4 in directory4:
                                            if file4.name.endswith('metadata.json'):    # extract info from metadata
                                                with open(file4) as f:
                                                    data = f.read()
                                                parsed_json = json.loads(data)
                                                image_id = parsed_json['id']
                                                if image_id not in PlanetScope_IDs:
                                                    PlanetScope_IDs.append(image_id)
                                                    os.mkdir('../../' + image_id)
                                                shutil.move(file4, directoryname+'/PlanetScope/'+image_id)
                                    with os.scandir(os.getcwd()) as directory4:
                                        for file4 in directory4:
                                            shutil.move(file4, directoryname+'/PlanetScope/'+image_id)
                                    os.chdir('..')
                        os.chdir('..')

            # delete the now empty folders and unnecessary files
            with os.scandir(os.getcwd()) as directory2:
                for file2 in directory2:
                    if file2.is_dir and file2.name not in PlanetScope_IDs:
                        shutil.rmtree(file2, ignore_errors=True)

            # Move image ID folders to date folders
            with os.scandir(os.getcwd()) as directory2:
                for file2 in directory2:
                    if file2.is_dir and file2.name.endswith('Store') == False:
                        date = file2.name[0:4]+'_'+file2.name[4:6]+'_'+file2.name[6:8]
                        if date not in PlanetScope_dates:
                            PlanetScope_dates.append(date)
                            os.mkdir(date)
                        shutil.move(file2, date)

os.chdir(directoryname)

# Organize SkySat folders


os.chdir(directoryname)

print('PlanetScope IDs: '+str(PlanetScope_IDs))
print('PlanetScope dates: '+str(PlanetScope_dates))
