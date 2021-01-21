import json
from pathlib import Path

annots_path = Path('MOT20Det-coco/MOT20-05/gt/instances_default.json')
new_annots_path = Path('MOT20Det-coco/MOT20-05/gt/instances_default_new.json')

TO_COMBINE = ['Static person', 'Pedestrian']
COMBINE_TO = 'Pedestrian'

with open(str(annots_path)) as json_file:
    coco_data = json.load(json_file)

new_categories = []
num_removed = 0
removed_first = False
combined_id = 0
id_change = {}

for category in coco_data["categories"]:
    cat_name = category["name"]
    cat_id = category["id"]

    if cat_name in TO_COMBINE and not removed_first:
    	category["name"] = COMBINE_TO
    	removed_first = True
    	combined_id = cat_id
    	new_categories.append(category)

    elif cat_name in TO_COMBINE:
    	num_removed += 1
    	id_change[cat_id] = combined_id

    else:
    	new_id = cat_id - num_removed
    	category["id"] = new_id
    	new_categories.append(category)
    	id_change[cat_id] = new_id

coco_data["categories"] = new_categories

annots = coco_data["annotations"]

for annot in annots:
	cat_id = annot["category_id"]
	if cat_id in id_change:
		annot["category_id"] = id_change[cat_id]

coco_data["annotations"] = annots

with open(str(new_annots_path), 'w') as json_file:
	json.dump(coco_data, json_file)
