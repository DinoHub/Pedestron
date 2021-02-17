import argparse
import json
from pathlib import Path

import cv2
from datumaro.components.project import Project


ap = argparse.ArgumentParser()
ap.add_argument('--json_path', type=str, help='annotations json path', required=True)
ap.add_argument('--src_folder', type=str, help='source folder path containing images', required=True)
ap.add_argument('--dest_folder', type=str, help='destination folder path to save blacked images', required=True)
args = ap.parse_args()

src_folder = Path(args.src_folder)
dest_folder = Path(args.dest_folder)
dest_folder.mkdir(parents=True, exist_ok=True)

project = Project() # create Datumaro project
project.add_source('src1', {'url': args.json_path, 'format': 'coco_instances'}) # add source
dataset = project.make_dataset() # create a dataset

color = (104, 116, 124) # imagenet means in bgr (0.406, 0.456,0.485)
thickness = -1
for item in dataset:
    # print(item.id)
    # print(item.annotations)

    image = cv2.imread(str(src_folder / Path(f'{item.id}.jpg')))

    for annot in item.annotations:
    	if annot.label == 1:
    		# print(annot.points)
    		start_point = (int(annot.points[0]), int(annot.points[1]))
    		end_point = (int(annot.points[2]), int(annot.points[3]))
    		image = cv2.rectangle(image, start_point, end_point, color, thickness) 

    filename = dest_folder / Path(f'{item.id}.jpg')
    filename.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(filename), image)
