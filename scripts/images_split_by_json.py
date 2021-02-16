import argparse
import json
from pathlib import Path
import shutil

ap = argparse.ArgumentParser()
ap.add_argument('--json_path', type=str, help='annotations json path', required=True)
ap.add_argument('--src_folder', type=str, help='source folder path containing all images', required=True)
ap.add_argument('--dest_folder', type=str, help='destination folder path to move all images contained in json', required=True)
args = ap.parse_args()

src_folder = Path(args.src_folder)
dest_folder = Path(args.dest_folder)
dest_folder.mkdir(parents=True, exist_ok=True)

with open(args.json_path) as json_file:
    annots = json.load(json_file)

for image in annots['images']:
    file_name = image["file_name"]
    print(file_name)

    my_file = src_folder / Path(f'{file_name}')
    to_file = dest_folder / Path(f'{file_name}')

    shutil.copyfile(my_file, to_file)
