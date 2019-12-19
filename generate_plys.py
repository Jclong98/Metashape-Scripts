import csv
import datetime
import os
import sys
import tkinter.filedialog as fd

import Metashape


def generate_ply(filepath, output_dir):
    """
    uses metashape to read a professor clipped file, find the 
    filepaths, add the images to a chunk, and generate a dense 
    cloud out of it

    parameters:
        filepath (str): a filepath the a professor clipped csv
        output_dir (str): a directory to where the ply generated from this file will end up

    returns:
        none
    """
    # building path to save to
    basename = os.path.basename(filepath)
    basename = os.path.splitext(basename)[0]
    filename = basename + '.ply'
    save_path = os.path.join(output_dir, filename)
    print("################################################")
    print(save_path)
    print("################################################")

    # creating a chunk to work with
    chunk = Metashape.app.document.addChunk()
    chunk.label = basename

    with open(filepath, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        # paths = [row['filepath'].replace("Images", "Images_no_exif") for row in csvreader]
        # paths = [row['filepath'] for row in csvreader]
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

    # Generate depth maps for the chunk.
    chunk.buildDepthMaps(quality=Metashape.MediumQuality, filter=Metashape.AggressiveFiltering)

    # generating the cloud
    chunk.buildDenseCloud()

    # saving
    chunk.exportPoints(save_path)

    print("done processing. point cloud exported to " + output_dir)

def generate_batch(run_dir, output_dir):
    """
    calls generate_ply() for each clipped csv in a professor run directory

    parameters:
        run_dir (str): a directory to a professor run. must contain a 'clipped' folder
        output_dir (str): a directory to where the plys generated from this run will end up

    returns:
        none
    """

    start_time = datetime.datetime.now()

    files_processed = 0

    for root, dirs, files in os.walk(run_dir):
        for f in files:
            if f.endswith('.csv') and 'plot' in f.lower():
                generate_ply(os.path.join(root, f), output_dir)
                files_processed += 1

    print("\nfiles processed: {}".format(files_processed))
    print("time elapsed: {}".format(datetime.datetime.now() - start_time))
    input("press any key to quit")


arg = sys.argv[1]

if os.path.isdir:
    generate_batch(
        os.path.join(arg, "clipped"),
        os.path.join(arg, "plot_plys")
    )
else:
    generate_ply(
        arg,
        os.path.join(os.path.split(os.path.split(arg)[0])[0], 'plot_plys')
    )
