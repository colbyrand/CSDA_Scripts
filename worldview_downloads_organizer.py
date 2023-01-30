##################################################################################
#                           Worldview Downloads Organizer

# Written by Colby Rand
# 2023/01/30

# This script takes the files downloaded by the Worldview bulk downloads API and
# organizes them in the following hierarchy: date -> image ID -> all files. The
# scripts accepts both zip files and uncompressed folders. The Worldview data
# comes in two formats: those delivered from the CSDA archive and those delivered
# from USGS. The zip files or folders that follow the "WV03_104001004B33DB00_M1BS"
# format are from the CSDA archive, whereas those folders and files that follow the
# "WV220190921193429M00" format were not in the CSDA archive and so were requested
# from the USGS.

# Before running this script, make sure all of the zip files or folders that need to
# be processed are located in a single folder. You must also install BeautifulSoup
# alongside the lxml xml parser using following commands:

# pip install beautifulsoup4
# pip install lxml

# Run the script by calling python from the terminal and then selecting the folder
# with the imagery that needs processing:

# python worldview_downloads.py

##################################################################################

import os
from tkinter import filedialog as fd
import tkinter as tk
import tarfile
import shutil
from zipfile import ZipFile
from bs4 import BeautifulSoup

# Get rid of tkinter root window
root = tk.Tk()
root.withdraw()

# Ask which folder needs to be processed
directoryname = fd.askdirectory()
os.chdir(directoryname)

# Initialize lists used to store the unique dates and catelog IDs encountered
dates = []
catids = []

# Uncompress all the zip files
with os.scandir(os.getcwd()) as directory:
    for file in directory:
        file_name = file.name
        if file_name.endswith('.zip'):
            print('Extracting: ' + file_name + '...')
            # for some reason, the USGS files could only be uncompressed using
            # zipfile commands, while the CSDA files could only be uncompressed
            # using tarfile commands, hense the try-except statements below
            try:
                with ZipFile(os.getcwd()+'/'+file_name, 'r') as f:  #USGS files
                    f.extractall(file_name[:-4])
            except:
                pass
            try:
                zippedfile = tarfile.open(os.getcwd()+'/'+file_name) #CSDA files
                zippedfile.extractall(os.getcwd()+'/'+file_name[:-4])
            except:
                pass

# Organize the files delivered by USGS
print('Organizing folders...')
with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.name.startswith('WV') and file.is_dir():
            date = file.name[3:7]+'_'+file.name[7:9]+'_'+file.name[9:11]
            if date not in dates:
                dates.append(date)
                os.mkdir(date)
            shutil.move(file,date)
            os.chdir(date+'/'+file.name)
            with os.scandir(os.getcwd()) as directory2:
                for file2 in directory2:
                    if file2.name.startswith(file.name[5:7]):
                        os.chdir(file2)
                        with os.scandir(os.getcwd()) as directory3:
                            for file3 in directory3:
                                if file3.name.endswith('.XML'):
                                    with open(file3, 'r') as f:
                                        data = f.read()
                                    bs_data = BeautifulSoup(data, 'xml')
                                    catid = str(bs_data.find('CATID'))
                                    catid_parsed = catid[7:23]
                                    if catid_parsed not in catids:
                                        catids.append(catid_parsed)
                                        os.mkdir('../../'+catid_parsed)
                        os.chdir('..')
            os.chdir('..')
            shutil.move(os.getcwd()+'/'+file.name, os.getcwd()+'/'+catid_parsed)
            os.chdir('..')

# Organize the files delivered by CSDA
with os.scandir(os.getcwd()) as directory:
    for file in directory:
        if file.name.startswith('1') and file.is_dir():
            os.chdir(os.getcwd()+'/'+file.name+'/'+file.name)
            with os.scandir(os.getcwd()) as directory2:
                for file2 in directory2:
                    if file2.name.endswith('.jpg'):
                        date2 = file2.name[5:9]+'_'+file2.name[9:11]+'_'+file2.name[11:13]
            os.chdir('../..')
            if date2 not in dates:
                os.mkdir(date2)
                dates.append(date2)
            catid = file.name[0:16]
            if catid not in catids:
                os.mkdir(date2+'/'+catid)
                catids.append(catid)
            shutil.move(os.getcwd()+'/'+file.name+'/'+file.name, os.getcwd()+'/'+date2+'/'+catid)
            os.rmdir(os.getcwd()+'/'+file.name)

# Output a summary of the dates and image IDs organized
print('Your imagery contained the following dates and image IDs:')
print('Dates: ')
for x in range(len(dates)):
    print('    '+dates[x])
print('Image IDs: ')
for x in range(len(catids)):
    print('    '+catids[x])