from bs4 import BeautifulSoup
import requests
import os
from PIL import Image
from io import BytesIO
import json
from tqdm import tqdm
import time

main_url = "http://platesmania.com"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}

count = 918
dict_json = {}
with open("images_annotations.json", "r+") as json_file:
    data = json.load(json_file)

    loop = tqdm(range(101), total=len(range(200)), leave=False)
    for i in loop:
        if i == 0:
            main_gallery_url = "http://platesmania.com/ua/gallery"
        else:
            main_gallery_url = f"http://platesmania.com/ua/gallery-{i}"

        gallery_page = requests.get(main_gallery_url, headers=headers)
        # Create soup object of url with images gallery
        gallery_soup = BeautifulSoup(gallery_page.content, 'html.parser')
        # Find all margins between images
        margins = gallery_soup.find_all(class_="row margin-bottom-10")
        for margin in margins:
            # Take url of each car in the gallery for further downloading and getting info about car
            gallery_img_urls = margin.find_all(class_="img-responsive center-block")
            for image_url in gallery_img_urls:
                # Select image ulr from dict
                image = image_url["src"]
                # Change url to images with big resolution
                image = image.replace("/m/", "/o/")
                # Select car/user id and assemble url of interested car
                car_id = image.split("/")[-1].split(".")[0]
                car_url = main_url + "/ua/nomer" + car_id

                # Create request to the url with car info and create soup object
                car_page = requests.get(car_url, headers=headers)
                car_soup = BeautifulSoup(car_page.content, 'html.parser')

                # Find h1 text which is a number plate of a car
                number_plate = car_soup.select('h1.pull-left')[0].text.strip()
                number_plate = number_plate.replace(" ", "_")

                # Create request to the image url of car, convert from bytes to readable format for Pillow
                image_savefile = str(count).zfill(5) + ".jpg"
                image_path = os.path.join("images", image_savefile)
                count += 1
                image = requests.get(image, headers=headers)
                img = BytesIO(image.content)
                img = Image.open(img)
                img.save(image_path)

                # Find car details (brand, model) using soup object of car url
                column_content = car_soup.find(class_="col-md-6 col-sm-7")
                img_content = column_content.find(class_="row").find("img")
                license_plate, car_desc = img_content['title'].split(",")
                car_desc = car_desc.strip()
                car_desc = car_desc.split(" ")

                # Process and save car info to string
                car_make = ""
                car_model = ""
                if len(car_desc) > 1:
                    car_make = car_desc[0]
                    car_model = " ".join(map(str, car_desc[1:]))
                    # Collect all info about car into dict
                    dict_json[number_plate] = {"image_path": image_path,
                                               "car_make": car_make,
                                               "car_model": car_model}
                else:
                    car_make = car_desc[0]
                    dict_json[number_plate] = {"image_path": image_path,
                                               "car_make": car_make}
                data.update(dict_json)
                json_file.seek(0)
                json.dump(data, json_file, indent=4, sort_keys=True)

        loop.set_description(f"Pages [{i}/200]")




