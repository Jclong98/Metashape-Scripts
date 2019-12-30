import csv
import datetime
import math
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
filename = basename + ".ply"

save_path = os.path.join(
    os.path.join(os.path.split(os.path.split(filepath)[0])[0], "plot_plys"),
    filename,
)

print(save_path)

# creating a chunk to work with
chunk.label = basename

with open(filepath, "r") as csvfile:
    csvreader = csv.DictReader(csvfile)

    n1_paths = []
    n2_paths = []
    n3_paths = []

    for row in csvreader:
        if "gopro" not in row["filepath"].lower():
            if "n1" in row["filepath"].lower():
                n1_paths.append(row["filepath"])

            if "n2" in row["filepath"].lower():
                n2_paths.append(row["filepath"])

            if "n3" in row["filepath"].lower():
                n3_paths.append(row["filepath"])

# loading the n2 images first so that the top camera is
# the one seen first and the point cloud won't end up rotated
paths = n2_paths + n3_paths + n1_paths

# add photos from csv here
chunk.addPhotos(paths)

# disabling exif gps data
for camera in chunk.cameras:
    camera.reference.enabled = False

# creating a local coordinate system
chunk.crs = Metashape.CoordinateSystem()

# Perform image matching for the chunk frame.
chunk.matchPhotos(
    accuracy=Metashape.HighAccuracy,
    generic_preselection=True,
    reference_preselection=False,
    tiepoint_limit=10000,
)

chunk.alignCameras()


print("ALIGNING COORDINATE SYSTEM BOUNDING BOX")
# https://github.com/agisoft-llc/metashape-scripts/blob/master/src/coordinate_system_to_bounding_box.py
R = chunk.region.rot  # Bounding box rotation matrix
C = chunk.region.center  # Bounding box center vector

if chunk.transform.matrix:
    T = chunk.transform.matrix
    s = math.sqrt(
        T[0, 0] ** 2 + T[0, 1] ** 2 + T[0, 2] ** 2
    )  # scaling # T.scale()
    S = Metashape.Matrix().Diag([s, s, s, 1])  # scale matrix
else:
    S = Metashape.Matrix().Diag([1, 1, 1, 1])

T = Metashape.Matrix(
    [
        [R[0, 0], R[0, 1], R[0, 2], C[0]],
        [R[1, 0], R[1, 1], R[1, 2], C[1]],
        [R[2, 0], R[2, 1], R[2, 2], C[2]],
        [0, 0, 0, 1],
    ]
)

chunk.transform.matrix = S * T.inv()  # resulting chunk transformation matrix
print("FINISHED ALIGNING COORDINATE SYSTEM BOUNDING BOX")

# Generate depth maps for the chunk.
chunk.buildDepthMaps(
    quality=Metashape.MediumQuality, filter=Metashape.AggressiveFiltering
)

# generating the cloud
chunk.buildDenseCloud()

# saving point cloud 
chunk.exportPoints(save_path)
