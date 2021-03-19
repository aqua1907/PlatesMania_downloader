import os
import json
import numpy as np

with open(r"lp_annotations1.json") as json_obj:
    data = json.load(json_obj)
json_obj.close()

items = []
for image_info in data["images"]:
    image_name = image_info['file_name']
    image_id = image_info["id"]

    for annotation in data["annotations"]:
        item = {}
        if annotation["image_id"] == image_id:
            if annotation["category_id"] == 1:
                if annotation["segmentation"] is not None:
                    polygons = annotation["segmentation"]
                    polygons = np.array(polygons).reshape((4, 2)).tolist()
                    item['image_name'] = image_name
                    item['labels'] = []
                    item['labels'].append({"class_name": "license_plate",
                                           "polygon": polygons})
                    items.append(item)
                else:
                    x, y, w, h = annotation["bbox"]
                    lp_bbox = [x, y, x + w, y + h]
                    item['image_name'] = image_name
                    item['labels'] = []
                    item['labels'].append({"class_name": "license_plate",
                                           "bbox": lp_bbox})
                    items.append(item)
            if annotation["category_id"] == 2:
                x, y, w, h = annotation["bbox"]
                car_bbox = [x, y, x + w, y + h]
                item['image_name'] = image_name
                item['labels'] = []
                item['labels'].append({"class_name": "car",
                                       "bbox": car_bbox})
                items.append(item)


with open(r"hasty_annotations.json", "w") as json_obj:
    json.dump(items, json_obj, indent=4)
json_obj.close()