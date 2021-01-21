import json
from pathlib import Path
import shutil

annots_path = Path('CrowdHuman/crowdhuman-train.json')

with open(str(annots_path)) as json_file:
    annots = json.load(json_file)

for image in annots['images']:
    file_name = image["file_name"]
    print(file_name)

    my_file = Path(f'CrowdHuman/Images/{file_name}')
    to_file = Path(f'CrowdHuman/train/{file_name}')

    shutil.copy(my_file, to_file)
