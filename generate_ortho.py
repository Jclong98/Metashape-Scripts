import csv
import datetime
import os
import sys
import tkinter.filedialog as fd

import Metashape

filepath = sys.argv[1]

# creating a chunk to work with
chunk = Metashape.app.document.addChunk()

with open(filepath, "r") as csvfile:
    csvreader = csv.DictReader(csvfile)
    paths = [
        row["filepath"].replace("Images", "Images_no_exif")
        for row in csvreader
    ]

# add photos from csv here
chunk.addPhotos(paths)

# Perform image matching for the chunk frame.
chunk.matchPhotos(
    accuracy=Metashape.HighAccuracy,
    generic_preselection=True,
    reference_preselection=False,
)
chunk.alignCameras()

# Generate depth maps for the chunk.
chunk.buildDepthMaps(
    quality=Metashape.MediumQuality, filter=Metashape.AggressiveFiltering
)

chunk.buildModel(
    surface=Metashape.Arbitrary, interpolation=Metashape.EnabledInterpolation
)
