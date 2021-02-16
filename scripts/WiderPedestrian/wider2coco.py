import argparse
import json
from pathlib import Path

from PIL import Image

INFO = {
	"contributor": "", 
	"date_created": "", 
	"description": "", 
	"url": "", 
	"version": "", 
	"year": ""
}

LICENSES = [
    {
    	"name": "", 
    	"id": 0, 
    	"url": ""
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'person',
        'supercategory': 'person',
    },
    {
        'id': 2,
        'name': 'ignore',
        'supercategory': 'ignore',
    },
]


def extract_txt_info(annots):
	for annot in annots:
		name_ann = annot.split(' ')
		img_name = name_ann[0]
		img_annots = [int(i) for i in name_ann[1:]]
		yield img_name, img_annots


ap = argparse.ArgumentParser()
ap.add_argument('--bbox_txt', help='bbox annotations path', required=True)
ap.add_argument('--ignore_txt', help='ignore annotations path', required=True)
ap.add_argument('--output_json', help='path of output annotation file in coco format', required=True)
args = ap.parse_args()

input_txt = Path(args.bbox_txt)
assert input_txt.is_file(), 'input txt does not exist.'
with open(input_txt, 'r') as file:
    lines = file.readlines()
input_stripped = [line.strip('\n') for line in lines]

ignore_txt = Path(args.ignore_txt)
assert ignore_txt.is_file(), 'input txt does not exist.'
with open(ignore_txt, 'r') as file:
    lines = file.readlines()
ignore_stripped = [line.strip('\n') for line in lines]
ignore_dict = dict(extract_txt_info(ignore_stripped))

json_dict = {"info": INFO, "licenses": LICENSES, "categories": CATEGORIES, "images": [], "annotations": []}
output_images = []
output_annotations = []

for img_name, img_annots in extract_txt_info(input_stripped):
	ignore_annots = ignore_dict.get(img_name, [])

	if len(ignore_annots):
		continue

	# images info
	if img_name.startswith('ad'):
		img = Image.open("/media/data/datasets/PersDet/WiderPedestrian_street/images/" + img_name)
	else:
		img = Image.open("/media/data/datasets/PersDet/WiderPedestrian_cctv/images/" + img_name)
	image_id = len(output_images)+1
	image_info = {'id': image_id, 
				  'file_name': img_name, 
				  'height': img.size[1], 
				  'width': img.size[0]
				 }
	output_images.append(image_info)

	# bbox annotations info
	for i in range(0, len(img_annots), 4):
		bbox_annots = img_annots[i:i+4]
		area = bbox_annots[2] * bbox_annots[3]
		annotation_info = {"id": len(output_annotations)+1, 
						   "image_id": image_id, 
						   "category_id": 1, 
						   "segmentation": [], 
						   "area": area, 
						   "bbox": bbox_annots, 
						   "iscrowd": 0, 
						   "attributes": {"occluded": False}}
		output_annotations.append(annotation_info)

# print(output_images)
# print(output_annotations)
json_dict["images"] = output_images
json_dict["annotations"] = output_annotations

with open(args.output_json, 'w') as outfile:
    json.dump(json_dict, outfile)
