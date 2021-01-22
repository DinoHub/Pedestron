import json
from pathlib import Path

annots_path = Path('instances_default.json')
new_annots_path = Path('instances_default_new.json')

TO_REMOVE_RANGE = [1972, 2151] # remove imgs from 001972.jpg to 002151.jpg inclusive

with open(str(annots_path)) as json_file:
    coco_data = json.load(json_file)

new_images = []
images_removed = 0
id_change = {}

for image in coco_data["images"]:
    img_name = image["file_name"]
    img_id = image["id"]

    # preprocess img_name to find in TO_REMOVE_RANGE
    extract_num = int(img_name.split('/')[-1].split('.')[0])

    if TO_REMOVE_RANGE[0] <= extract_num <= TO_REMOVE_RANGE[1]:
        images_removed += 1
        id_change[img_id] = 0
        print(img_name)

    else:
        new_id = img_id - images_removed
        image["id"] = new_id
        new_images.append(image)
        id_change[img_id] = new_id

coco_data["images"] = new_images

annots = coco_data["annotations"]
new_annots = []
annotations_removed = 0

for annot in annots:
    img_id = annot["image_id"]
    annot_id = annot["id"]

    if id_change[img_id] == 0:
        annotations_removed += 1
    else:
        new_annot_id = annot_id - annotations_removed
        annot["id"] = new_annot_id
        annot["image_id"] = id_change[img_id]
        new_annots.append(annot)

coco_data["annotations"] = new_annots

with open(str(new_annots_path), 'w') as json_file:
    json.dump(coco_data, json_file)
