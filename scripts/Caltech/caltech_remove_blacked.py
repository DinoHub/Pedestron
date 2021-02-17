import argparse
import json
# from pathlib import Path

from datumaro.components.project import Project
from datum_utils import num_img, num_img_with_annots, num_annots, export_json


def check_overlap(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both rectangles
    # boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection area and dividing it by the union area
    # iou = interArea / float(boxAArea + boxBArea - interArea)

    # compute overlap by taking intersection area and dividing it by boxB area
    overlap = interArea / boxBArea

    return overlap


ap = argparse.ArgumentParser()
ap.add_argument('--json_path', type=str, help='annotations json path', required=True)
ap.add_argument('--output_json', default='', help='path of output json. overwrite input json if not specified')
args = ap.parse_args()

project = Project() # create Datumaro project
project.add_source('src1', {'url': args.json_path, 'format': 'coco_instances'}) # add source
dataset = project.make_dataset() # create a dataset

annot_ids_to_filter = []
for item in dataset:
    for annot in item.annotations:
        if annot.label == 1:
            # check all annotations (including ownself) in image and remove those with overlap > 0.5
            for img_annot in item.annotations:
                overlap = check_overlap(annot.points, img_annot.points)
                if overlap > 0.5:
                    annot_ids_to_filter.append(img_annot.id)
                    img_annot.attributes["to_remove"] = True

dataset1 = dataset.filter(f"/item/annotation[not(to_remove='True')]", filter_annotations=True)
print(f'num annots to filter: {len(set(annot_ids_to_filter))}')
print(f'num annotations before: {num_annots(dataset)}')
print(f'num annotations after: {num_annots(dataset1)}')

# export the resulting dataset in COCO format
export_json(dataset1, args.output_json, args.json_path)
