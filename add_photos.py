import csv
import datetime
import os
import sys

import Metashape

filepath = sys.argv[1]

print(filepath)

# creating a chunk to work with
chunk = Metashape.app.document.addChunk()

# building path to save to
basename = os.path.basename(filepath)
basename = os.path.splitext(basename)[0]
filename = basename + '.ply'

# creating a chunk to work with
chunk.label = basename

with open(filepath, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    # paths = [row['filepath'].replace("Images", "Images_no_gps") for row in csvreader]
    paths = [row['filepath'] for row in csvreader if "gopro" not in row['filepath'].lower()]

# add photos from csv here
chunk.addPhotos(paths)

# disabling exif gps data
for camera in chunk.cameras:
    camera.reference.enabled = False

# creating a local coordinate system
chunk.crs = Metashape.CoordinateSystem()

# Perform image matching for the chunk frame.
chunk.matchPhotos(accuracy=Metashape.HighAccuracy, generic_preselection=True, reference_preselection=False, tiepoint_limit=10000)

chunk.alignCameras()