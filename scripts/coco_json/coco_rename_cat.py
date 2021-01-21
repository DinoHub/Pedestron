import json
from pathlib import Path

annots_path = Path('instances_default.json')
new_annots_path = Path('instances_default_new.json')

with open(str(annots_path)) as json_file:
    annots = json.load(json_file)

cats = annots["categories"]

for cat in cats:
	if cat["name"] == 'pedestrain':
		cat["name"] = 'pedestrian'
		cat["supercategory"] = 'pedestrian'

annots["categories"] = cats

with open(str(new_annots_path), 'w') as json_file:
	json.dump(annots, json_file)
