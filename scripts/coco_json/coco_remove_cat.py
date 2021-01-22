import json
from pathlib import Path

annots_path = Path('instances_default.json')
new_annots_path = Path('instances_default_new.json')

TO_REMOVE = ['mask']

with open(str(annots_path)) as json_file:
    coco_data = json.load(json_file)

new_categories = []
num_removed = 0
id_change = {}

for category in coco_data["categories"]:
    cat_name = category["name"]
    cat_id = category["id"]

    if cat_name in TO_REMOVE:
        num_removed += 1
        id_change[cat_id] = 0

    else:
        new_id = cat_id - num_removed
        category["id"] = new_id
        new_categories.append(category)
        id_change[cat_id] = new_id

coco_data["categories"] = new_categories

annots = coco_data["annotations"]
new_annots = []
annotations_removed = 0

for annot in annots:
    cat_id = annot["category_id"]
    annot_id = annot["id"]

    if id_change[cat_id] == 0:
        annotations_removed += 1
    else:
        new_annot_id = annot_id - annotations_removed
        annot["id"] = new_annot_id
        annot["category_id"] = id_change[cat_id]
        new_annots.append(annot)

coco_data["annotations"] = new_annots

with open(str(new_annots_path), 'w') as json_file:
    json.dump(coco_data, json_file)
