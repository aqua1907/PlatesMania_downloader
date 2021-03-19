import json
import pprint
import cv2
import os
import numpy as np
from PIL import Image

with open(r"lp_annotations.json") as json_obj:
    data = json.load(json_obj)
json_obj.close()

list_images = []
for image_info in data["images"]:
    image = {"image": image_info["file_name"]}
    path = os.path.join("images", image_info["file_name"])
    img = np.array(Image.open(path))
    img_copy = img.copy()
    image_id = image_info["id"]

    car_count = 0
    lp_count = 0
    image["cars"] = {}
    for annotation in data["annotations"]:
        if annotation["image_id"] == image_id:
            if annotation["category_id"] == 2:
                if annotation["segmentation"] is not None:
                    polygon = annotation["segmentation"]
                    lp_polygon = polygon
                    lp_count += 1
                else:
                    x, y, w, h = annotation["bbox"]
                    x1, y1, x2, y2 = x, y, x + w, y + h
                    lp_bbox = [x1, y1, x2, y2]
                    lp_count += 1
            if annotation["category_id"] == 1:
                x, y, w, h = annotation["bbox"]
                x1, y1, x2, y2 = x, y, x + w, y + h
                car_bbox = [x1, y1, x2, y2]
                car_count += 1

            if lp_count / 2 == 1:
                if "car_1" in image["cars"]:
                    image["cars"]["car_1"]["lp_polygon"] = lp_polygon
                    image["cars"]["car_1"]["lp_bbox"] = lp_bbox
                else:
                    image["cars"]["car_1"] = {"lp_polygon": lp_polygon,
                                              "lp_bbox": lp_bbox}
            elif lp_count / 2 == 2:
                if "car_2" in image["cars"]:
                    image["cars"]["car_2"]["lp_polygon"] = lp_polygon
                    image["cars"]["car_2"]["lp_bbox"] = lp_bbox
                else:
                    image["cars"]["car_2"] = {"lp_polygon": lp_polygon,
                                              "lp_bbox": lp_bbox}
            elif lp_count / 2 == 3:
                if "car_3" in image["cars"]:
                    image["cars"]["car_3"]["lp_polygon"] = lp_polygon
                    image["cars"]["car_3"]["lp_bbox"] = lp_bbox
                else:
                    image["cars"]["car_3"] = {"lp_polygon": lp_polygon,
                                              "lp_bbox": lp_bbox}
            elif lp_count / 2 == 4:
                if "car_4" in image["cars"]:
                    image["cars"]["car_4"]["lp_polygon"] = lp_polygon
                    image["cars"]["car_4"]["lp_bbox"] = lp_bbox
                else:
                    image["cars"]["car_4"] = {"lp_polygon": lp_polygon,
                                              "lp_bbox": lp_bbox}
            if car_count == 1:
                if "car_1" in image["cars"]:
                    image["cars"]["car_1"]["car_bbox"] = car_bbox
                else:
                    image["cars"]["car_1"] = {"car_bbox": car_bbox}
            elif car_count == 2:
                if "car_2" in image["cars"]:
                    image["cars"]["car_2"]["car_bbox"] = car_bbox
                else:
                    image["cars"]["car_2"] = {"car_bbox": car_bbox}
            elif car_count == 3:
                if "car_3" in image["cars"]:
                    if "car_3" in image["cars"]:
                        image["cars"]["car_3"]["car_bbox"] = car_bbox
                    else:
                        image["cars"]["car_3"] = {"car_bbox": car_bbox}
            elif car_count == 4:
                if "car_4" in image["cars"]:
                    if "car_4" in image["cars"]:
                        image["cars"]["car_4"]["car_bbox"] = car_bbox
                    else:
                        image["cars"]["car_4"] = {"car_bbox": car_bbox}
    list_images.append(image)

with open(r"inputs/wpod_net/annot_for_wpodnet.json", "w") as file_obj:
    json.dump(list_images, file_obj, indent=4)
file_obj.close()
