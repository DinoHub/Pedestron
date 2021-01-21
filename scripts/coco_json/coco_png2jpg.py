import json
from pathlib import Path

annots_path = Path('instances_default.json')
new_annots_path = Path('instances_default_new.json')

with open(str(annots_path)) as json_file:
    annots = json.load(json_file)

images = annots["images"]

for image in images:
    file_name = image["file_name"]
    new_name = f"{file_name.split('.')[0]}.jpg"

    image["file_name"] = new_name

annots["images"] = images

with open(str(new_annots_path), 'w') as json_file:
	json.dump(annots, json_file)
