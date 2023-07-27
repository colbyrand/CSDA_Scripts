import os
import shutil
from tkinter import filedialog as fd
import tkinter as tk
import json
import csv

# Get rid of tkinter root window
root = tk.Tk()
root.withdraw()

# Ask which folder needs to be processed
directoryname = fd.askdirectory()
os.chdir(directoryname)

print('')

with open('metadata.csv', 'w', newline='') as metaFile:
    writer = csv.writer(metaFile)
    writer.writerow(['Image ID', 'Acquisition Date/Time', 'Region', 'Site', 'Tasked By', 'Product Type', 'Sensor Name', 'Sensor Angle', 'Integration Time', 'Reported Saturation Percentage'])

    with os.scandir(os.getcwd()) as directory:
        for file in directory:
            if file.is_dir():
                os.chdir(file)          # Enter year folder
                with os.scandir(os.getcwd()) as directory2:
                    for file2 in directory2:
                        if file2.is_dir():
                            os.chdir(file2)     # Enter date folder
                            with os.scandir(os.getcwd()) as directory3:
                                for file3 in directory3:
                                    
                                    # Area Coverage images
                                    if file3.name.endswith('AREA'):
                                        print('Area coverage: ' + os.getcwd())
                                        os.chdir(file3)         # Enter Area Coverage folder
                                        os.chdir('Anthro')      # Enter Anthro folder
                                        with os.scandir(os.getcwd()) as directory4:
                                            for file4 in directory4:
                                                if file4.name.endswith('.json') and file4.name.startswith('BSG'):
                                                    with open(file4) as f:
                                                        data = f.read()
                                                    parsed_json = json.loads(data)

                                                    id = parsed_json['id'][29:38]
                                                    acquisitionDate = parsed_json['acquisitionDate'][0:10]+' '+parsed_json['acquisitionDate'][11:19]+' UTC'
                                                    region = ''
                                                    site = ''
                                                    taskedBy = ''
                                                    productType = 'Area Coverage'
                                                    sensorName = parsed_json['sensorName']
                                                    offNadirAngle = ''
                                                    integrationTime = ''
                                                    fractionSaturated = str(parsed_json['fractionSaturated'])

                                                    writer.writerow([id, acquisitionDate, region, site, taskedBy, productType, sensorName, offNadirAngle, integrationTime, fractionSaturated])

                                                    print('Image ID: ' + id)
                                                    print('Acquisition Date/Time: ' + acquisitionDate)
                                                    print('Product Type: ' + productType)
                                                    print('Sensor Name: ' + sensorName)
                                                    print('Sensor Angle: ' + offNadirAngle)
                                                    print('Integration Time: ' + integrationTime)
                                                    print('Reported Saturation Percentage: ' + fractionSaturated)
                                                    print('')
                                            os.chdir('../..')

                                    # Either Standard or Frame images
                                    if file3.is_dir and not file3.name.endswith('AREA') and not file3.name.endswith('Store') and not file3.name.startswith('.'):
                                        print('Standard or frame: ' + os.getcwd())
                                        os.chdir(file3)         # Enter standard or frame folder
                                        os.chdir('Anthro')      # Enter Anthro folder
                                        with os.scandir(os.getcwd()) as directory4:
                                            for file4 in directory4:
                                                if file4.name.endswith('.json') and file4.name.startswith('BSG'):
                                                    with open(file4) as f:
                                                        data = f.read()
                                                    parsed_json = json.loads(data)

                                                    id = parsed_json['id'][24:33]
                                                    acquisitionDate = parsed_json['acquisitionDate'][0:10]+' '+parsed_json['acquisitionDate'][11:19]+' UTC'
                                                    region = ''
                                                    site = ''
                                                    taskedBy = ''
                                                    if 'multiImage' in parsed_json:
                                                        productType = 'Frame'
                                                    else:
                                                        productType = 'Standard'
                                                    sensorName = parsed_json['sensorName']
                                                    offNadirAngle = str(parsed_json['offNadirAngle'])
                                                    if 'integrationTime' in parsed_json:
                                                        integrationTime = str(parsed_json['integrationTime'])
                                                    else:
                                                        integrationTime = ''
                                                    fractionSaturated = str(parsed_json['fractionSaturated'])

                                                    writer.writerow([id, acquisitionDate, region, site, taskedBy, productType, sensorName, offNadirAngle, integrationTime, fractionSaturated])

                                                    print('Image ID: ' + id)
                                                    print('Acquisition Date/Time: ' + acquisitionDate)
                                                    print('Product Type: ' + productType)
                                                    print('Sensor Name: ' + sensorName)
                                                    print('Sensor Angle: ' + offNadirAngle)
                                                    print('Integration Time: ' + integrationTime)
                                                    print('Reported Saturation Percentage: ' + fractionSaturated)
                                                    print('')
                                            os.chdir('../..')
                        os.chdir('..')
