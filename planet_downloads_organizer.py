##################################################################################
#                           Planet Downloads Organizer

# Written by Colby Rand
# 2023/02/18

# This script takes the files downloaded through Planet Explorer and organizes them
# in the following hierarchy: sensor -> date -> image ID -> all files. Before
# running this script, make sure all downloaded folders are located in a single
# folder. Run the script by calling python from the terminal and then selecting the
# folder with the imagery that needs processing:

# python planet_downloads_organizer.py

##################################################################################

import os
from tkinter import filedialog as fd
import tkinter as tk
import shutil
import tarfile
from zipfile import ZipFile

# Get rid of tkinter root window
root = tk.Tk()
root.withdraw()

# Ask which folder needs to be processed
directoryname = fd.askdirectory()
os.chdir(directoryname)

# Initialize lists used to store the unique dates and catelog IDs encountered
PlanetScope_dates = []
PlanetScope_catids = []
planetscope_present = 0     # variables to indicate if PlanetScope images were encountered

# Move image folders to PlanetScope folders
with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.is_dir():
            if 'psscene' in file.name:
                if planetscope_present == 0:
                    os.mkdir('PlanetScope')
                planetscope_present = 1
                shutil.move(os.getcwd()+'/'+file.name, os.getcwd()+'/PlanetScope')

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
                                if file3.name == 'files':
                                    os.chdir('files')     # enter files folder
                                    with os.scandir(os.getcwd()) as directory4:
                                        for file4 in directory4:        # loop through files in 'files' folder and create image ID folders in the PlanetScope folder
                                            if file4.name.endswith('Store') == False:
                                                id = file4.name.split('_')
                                                catid = str(id[0]) + '_' + str(id[1]) + '_' + str(id[2]) + '_' + str(id[3])
                                                if catid not in PlanetScope_catids:
                                                    PlanetScope_catids.append(catid)
                                                    print(catid)
                                                    os.mkdir('../../' + catid)
                                                os.chdir('../..')
                                                path=os.getcwd()
                                                os.chdir(file2.name+'/files')
                                                shutil.move(os.getcwd()+'/'+file4.name, path+'/'+catid)
                                    os.chdir('..')
                        os.chdir('..')
            with os.scandir(os.getcwd()) as directory2:     # delete the now empty folders and manifests
                for file2 in directory2:
                    if file2.is_dir and file2.name not in PlanetScope_catids:
                        shutil.rmtree(os.getcwd()+'/'+file2.name, ignore_errors=True)
            # Move image ID folders to date folders
            with os.scandir(os.getcwd()) as directory2:
                for file2 in directory2:
                    if file2.is_dir and file2.name.endswith('Store') == False:
                        date = file2.name[0:4]+'_'+file2.name[4:6]+'_'+file2.name[6:8]
                        if date not in PlanetScope_dates:
                            PlanetScope_dates.append(date)
                            os.mkdir(date)
                        shutil.move(file2.name, date)

os.chdir(directoryname)

print('PlanetScope IDs: '+str(PlanetScope_catids))
print('PlanetScope dates: '+str(PlanetScope_dates))
