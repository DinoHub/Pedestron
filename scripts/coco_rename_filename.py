import json
from pathlib import Path

annots_path = Path('CityPersons-coco/gtBbox_CityPersons_trainval/gtBboxCityPersons/citypersons-train.json')
new_annots_path = Path('CityPersons-coco/gtBbox_CityPersons_trainval/gtBboxCityPersons/citypersons-train_new.json')

with open(str(annots_path)) as json_file:
    annots = json.load(json_file)

images = annots["images"]

for image in images:
    file_name = image["file_name"]

    # new_name = file_name.split('/')[-1]

    # new_name = '/'.join(file_name.split('/')[-3:])

    city = file_name.split('_')[0]
    new_name = f'CityPersons-coco/leftImg8bit_trainvaltest/leftImg8bit/train/{city}/{file_name}'

    image["file_name"] = new_name

annots["images"] = images

with open(str(new_annots_path), 'w') as json_file:
	json.dump(annots, json_file)
