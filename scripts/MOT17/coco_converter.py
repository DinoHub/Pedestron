import os
import shutil
import pandas as pd
import json

MOT_label = ["Pedestrian", "Person on vehicle", "Car", "Bicycle", "Motorbike", "Non-motorized vehicle", "static person", "distractor",
             "occluder", "occluder on the ground", "occluder full", "reflection"]

def get_imgheader(folder):
    imgname = os.listdir(os.path.join(folder, 'images'))[0]
    return imgname[:imgname.rfind('_')], os.path.splitext(imgname)[-1]

def form_imgname(imgheader, frame, ext):
    frame = str(int(frame))
    num_of_zeros = '0' * (6 - len(frame))
    num_tag = num_of_zeros + frame + ext
    return '_'.join([imgheader, num_tag])

def mot_to_coco(folder):
    gt_path = os.path.join(folder, 'gt', 'gt.txt')
    df = pd.read_csv(gt_path, names=['frame', 'id', 'xmin', 'ymin', 'w', 'h', 'conf', 'class', 'visibility'])
    # i.e MOT17_04
    imgheader, ext = get_imgheader(folder)
    json_out = {'images': [], 'annotations': [], 'categories': [{'id': 1, 'name': 'person'}]}
    ann_id, image_id = 1, 1 
    image_id_dict = {}
    for _,item in df.iterrows():
        imgname = form_imgname(imgheader, item['frame'], ext)
        if imgname not in image_id_dict:
            image_id_dict[imgname] = image_id
            image_id += 1
        json_out['categories'] = [{'id': i+1, 'name': MOT_label[i]} for i in range(len(MOT_label))]
        
        # filtered to person only. Reflections are to be removed as discussed.
        if item['class'] in [1,2,7,8]:
            occluded = 'false' if item['visibility'] !=0 else 'true'
            json_out['annotations'].append({
                'id': ann_id,
                'image_id': image_id_dict[imgname],
                'category_id': 1,
                'iscrowd': 0,
                'bbox': [item['xmin'], item['ymin'], item['w'], item['h']],
                "attributes": {"occluded": occluded }
            })
            ann_id += 1
    json_out['images'] = [{'file_name': key, 'id': val} for key,val in image_id_dict.items()]
    json.dump(json_out, open(os.path.join(folder,'train.json'), 'w'))

def combine_json_in_folder(folder):
    json_out = {'images': [], 'annotations': [], 'categories': [{'id': 1, 'name': 'person'}]}
    ann_id, image_id = 1, 1
    image_id_converter = {}
    for dir in os.listdir(folder):
        json_path = os.path.join(folder, dir, 'train.json')
        json_in = json.load(open(json_path, 'r'))
        for img_dict in json_in['images']:
            old_image_id, filename = img_dict['id'], img_dict['file_name']
            json_out['images'].append({'file_name': filename, 'id': image_id})
            image_id_converter[old_image_id] = image_id
            image_id += 1
        for ann_dict in json_in['annotations']:
            ann_dict['iscrowd'] = 0
            ann_dict['id'] = ann_id
            ann_id += 1
            ann_dict['image_id'] = image_id_converter[ann_dict['image_id']]
            json_out['annotations'].append(ann_dict)
    json.dump(json_out, open(os.path.join(folder, 'train.json'), 'w'))
        

if __name__ == "__main__":
    '''
    inputs: <par>/MOT17-<XX>/gt/gt.txt & <par>/MOT17-<XX>/images/*
    outputs: train.json in <par>/MOT17-<XX>/train.json and par/train.json (merged)
    '''
    par_list = ['back_up_street/', 'backup_cctv/']
    for par in par_list:
        for dir in os.listdir(par):
            mot_to_coco(os.path.join(par,dir))
        combine_json_in_folder(par)