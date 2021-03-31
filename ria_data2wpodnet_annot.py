import json
import numpy as np
import cv2
import os
from scipy.spatial.distance import euclidean

with open(r"inputs/ria/via_region_data.json") as f:
    ria_data = json.load(f)
f.close()

with open(r"inputs/wpod_net/wpodnet_data.json") as f:
    main_data = json.load(f)
f.close()

last_filename = main_data[-1]["file_name"]
count = int(last_filename.split(".")[0]) + 1


for k, v in ria_data.items():
    if v["regions"]:
        dists = []

        filename = v["filename"]
        file_name_ext = filename.split(".")[-1]
        new_filename = str(count).zfill(5) + f".{file_name_ext}"
        count += 1

        image_path = os.path.join(r"inputs/ria/train", filename)
        img_orig = cv2.imread(image_path)
        img_copy = img_orig.copy()

        # cv2.imwrite(os.path.join(r"inputs/wpod_net/train", new_filename), img_orig)

        shape_attributes = v["regions"][0]["shape_attributes"]
        polygon_xs = shape_attributes["all_points_x"]
        polygon_ys = shape_attributes["all_points_y"]
        polygon = [[polygon_xs[0], polygon_ys[0], polygon_xs[1], polygon_ys[1],
                    polygon_xs[2], polygon_ys[2], polygon_xs[3], polygon_ys[3]]]
        points = np.array(polygon).reshape((4, 2))
        # for point in points[:2]:
        #     cv2.circle(img_orig, (int(point[0]), int(point[1])), 6, (255, 0, 0), 6)
        # cv2.imshow("orig", img_orig)

        for point in points:
            dist = euclidean([0, 0], point)
            dists.append(dist)

        dists = np.array(dists)

        tl_idx = np.argmin(dists)
        br_idx = np.argmax(dists)
        top_left = points[tl_idx]
        bottom_right = points[br_idx]
        dists = np.delete(dists, [tl_idx, br_idx])
        points = np.delete(points, [tl_idx, br_idx], axis=0)

        top_right = points[np.argmax(points[:, 0])]
        bottom_left = points[np.argmin(points[:, 0])]

        points = np.array([top_left, top_right, bottom_right, bottom_left])
        # for point in points[:2]:
        #     cv2.circle(img_copy, (int(point[0]), int(point[1])), 6, (255, 0, 0), 6)
        # cv2.imshow("copy", img_copy)
        # cv2.waitKey(0)
        points = points.reshape(1, 8).tolist()

        item_data = dict(file_name=new_filename,
                         polygon=points,
                         bbox=[])
        main_data.append(item_data)

with open(r"inputs/wpod_net/wpodnet_data_final.json", "w") as f:
    json.dump(main_data, f)
f.close()

