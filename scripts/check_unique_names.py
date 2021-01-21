import argparse
from pathlib import Path

from tqdm import tqdm

IMG_EXTS = ['.jpg','.jpeg','.png','.tiff','.tif','.bmp','.gif','.webp']
IMG_EXTS = [x.lower() for x in IMG_EXTS] + [x.upper() for x in IMG_EXTS]
print('Acceptable img extensions:', IMG_EXTS)

ap = argparse.ArgumentParser()
ap.add_argument('root')
args = ap.parse_args()

rootpath = Path(args.root)
filenames = []
for filepath in tqdm(list(rootpath.rglob('*'))):
    if filepath.suffix not in IMG_EXTS:
        continue
    if filepath.stem not in filenames:
        filenames.append(filepath.stem)
    else:
        print('Duplicate name detected:', filepath)

print('some example filenames:', filenames[:5], filenames[-5:])

print('Total images: ', len(filenames))
