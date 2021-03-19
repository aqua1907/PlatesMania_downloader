import json
import os
import cv2
import numpy as np


with open(r"inputs/wpod_net/annot_for_wpodnet.json") as f_obj:
    data = json.load(f_obj)
f_obj.close()

count = 0
wpodnet_data = []
for image in data:
    path = os.path.join("images", image["image"])
    img = cv2.imread(path)
    for k in image["cars"].keys():
        count += 1
        # car bbox
        x1_c, y1_c, x2_c, y2_c = image["cars"][k]["car_bbox"]
        crop_img = img[y1_c:y2_c, x1_c:x2_c]

        # clicnese plate bbox
        x1_lp, y1_lp, x2_lp, y2_lp = image["cars"][k]["lp_bbox"]
        x1_lp -= x1_c
        x2_lp -= x1_c
        y1_lp -= y1_c
        y2_lp -= y1_c

        # license plate polygon
        polygon = image["cars"][k]["lp_polygon"]
        points = np.array(polygon).reshape((4, 2))
        points[:, 0] -= x1_c
        points[:, 1] -= y1_c
        polygon = points.copy().reshape((-1, 8)).tolist()

        file_name = str(count).zfill(5) + ".jpg"
        new_path = os.path.join(r"inputs/wpod_net/train", file_name)
        cv2.imwrite(new_path, crop_img)
        wpodnet_item = dict(file_name=file_name,
                            polygon=polygon,
                            bbox=[x1_lp, y1_lp, x2_lp, y2_lp])
        wpodnet_data.append(wpodnet_item)

with open(r"inputs/wpod_net/wpodnet_data.json", "w") as f:
    json.dump(wpodnet_data, f, indent=4)
f.close()



