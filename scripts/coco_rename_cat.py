import json
from pathlib import Path

annots_path = Path('EuroCity_Persons/day/labels/eurocity-day_val_old.json')
new_annots_path = Path('EuroCity_Persons/day/labels/eurocity-day_val.json')

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
