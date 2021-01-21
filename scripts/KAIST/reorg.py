from pathlib import Path
from shutil import copy

from tqdm import tqdm

'''
train - Day : 0,1,2
train - Night : 3,4,5
test - Day : 6,7,8
test - Night : 9,10,11
'''

IMG_EXTS = ['.jpg','.jpeg','.png','.tiff','.tif','.bmp','.gif','.webp']
IMG_EXTS = [x.lower() for x in IMG_EXTS] + [x.upper() for x in IMG_EXTS]
print('Acceptable img extensions:', IMG_EXTS)

split_dict = {
            'day':{
                'train':[0,1,2],
                'val':[6],
                'test':[7,8]
                },
            'night':{
                'train':[3,4,5],
                'val':[9],
                'test':[10,11]
                }
            }

rootpath = Path('/media/dh/HDD/person/KAIST_Multispectral_Pedestrian_Detection_Benchmark')
out_dir = rootpath / 'KAIST_DH'

img_dir = rootpath / 'images'
set2imgpaths = {}
set2lwirpaths = {}

for set_dir in img_dir.glob('*'):
    set_num = int(set_dir.stem.split('set')[-1])
    
    imgpaths = []
    lwirpaths = []
    for ip in set_dir.rglob('*'):
        if ip.suffix in IMG_EXTS:
            if ip.parent.stem == 'lwir':
                lwirpaths.append(ip)
            elif ip.parent.stem == 'visible':
                imgpaths.append(ip)

    set2imgpaths[set_num] = imgpaths
    set2lwirpaths[set_num] = lwirpaths

xml_dir = rootpath / 'annotations-xml-181027'
set2xmlpaths = {}
for set_dir in xml_dir.glob('*'):
    set_num = int(set_dir.stem.split('set')[-1])
    
    xmlpaths = [ xp for xp in set_dir.rglob('*.xml') ]    
    set2xmlpaths[set_num] = xmlpaths

for mode, mode_dict in split_dict.items():
    mode_outpath = out_dir / mode
    img_outpath = mode_outpath / 'images'
    lwir_outpath = mode_outpath / 'lwir'
    xmls_outpath = mode_outpath / 'xmls'
    for sets in mode_dict.values():
        for set_num in sets:
            print(f'Set {set_num}')
            og_img_paths = set2imgpaths[set_num]
            for p in tqdm(og_img_paths):
                old_parents = p.parents
                new_name = f'{old_parents[2].stem}_{old_parents[1].stem}_{old_parents[0].stem}_{p.stem}{p.suffix}'
                new_path = img_outpath / new_name
                if not new_path.is_file():
                    copy(p, new_path)

            og_lwir_paths = set2lwirpaths[set_num]
            for p in tqdm(og_lwir_paths):
                old_parents = p.parents
                new_name = f'{old_parents[2].stem}_{old_parents[1].stem}_{old_parents[0].stem}_{p.stem}{p.suffix}'
                new_path = lwir_outpath / new_name
                if not new_path.is_file():
                    copy(p, new_path)

            og_xml_paths = set2xmlpaths[set_num]
            for p in tqdm(og_xml_paths):
                old_parents = p.parents
                new_name = f'{old_parents[2].stem}_{old_parents[1].stem}_{old_parents[0].stem}_{p.stem}{p.suffix}'
                new_path = xmls_outpath / new_name
                if not new_path.is_file():
                    copy(p, new_path)


import pdb; pdb.set_trace()