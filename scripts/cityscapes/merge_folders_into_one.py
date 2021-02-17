import os
import shutil 
from tqdm import tqdm
import json

def merge_folder_into_images(start_folder):
    for folder in tqdm(os.listdir(start_folder)):
        par_path = os.path.join(start_folder , folder)
        for image_path in os.listdir(par_path):
            shutil.move(os.path.join(par_path, image_path), os.path.join('images', image_path))
    print ("Done")

def merge_folder_json_into_one(start_folders):
    classes = ['ignore', 'pedestrian', 'rider', 'sitting person', 
    'person (other)','person group']

    json_output = {'images': [],
                 'categories': [{'id': 1, 'name': 'person'}],
                  'annotations': []}
    #json_output['categories'] = [dict(id=i+1, name=classname) for i, classname in enumerate(classes)]
    print (json_output['categories'])
    img_id, annotations_id = 1, 1
    for start_folder in start_folders:
        for folder in tqdm(os.listdir(start_folder)):
            par_path = os.path.join(start_folder , folder)
            for json_dir in os.listdir(par_path):
                raw_json = json.load(open(os.path.join(par_path, json_dir), 'r'))
                img_name = json_dir.replace('gtBboxCityPersons.json', 'leftImg8bit.png')

                json_output['images'].append(dict(
                    id=img_id,
                    width=raw_json['imgWidth'],
                    height=raw_json['imgHeight'],
                    file_name=img_name
                ))
                
                for ann in raw_json['objects']:
                    if ann['label'] != 'ignore':
                        json_output['annotations'].append(dict(
                            id=annotations_id,
                            image_id=img_id,
                            iscrowd=0,
                            bbox=ann['bbox'],
                            #category_id=classes.index(ann['label']) + 1
                            category_id=1
                        ))
                        annotations_id += 1
                img_id += 1
    json.dump(json_output, open('all.json', 'w'))
    print ('Done')

#merge_folder_into_images('val')
merge_folder_json_into_one(['gtBboxCityPersons/train', 'gtBboxCityPersons/val'])
