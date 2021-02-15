import json
import cv2 

coco_json = json.load(open('all.json'))

for item in coco_json['images']:
    img = cv2.imread('images/' + item['file_name'])
    h, w, c = img.shape
    item['height'] = h
    item['width'] = w

json.dump(coco_json, open('train_new.json', 'w'))


