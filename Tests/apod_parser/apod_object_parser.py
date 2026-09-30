import json
import os

from urllib.request import Request, urlopen, urlretrieve

# PIL (pillow) est utilisé pour convertir les images mais on n'en a plus besoin, ellles sont désormais toutes au format JPG
# from PIL import Image


def get_data(date) -> dict:
    with urlopen(f"https://science.nasa.gov/wp-json/wp/v2/apod-basic/{date}") as response:
        body = json.load(response)
    return body


def get_explaination(response):
    explaination = response["explanation"]
    return explaination


def get_hdurl(response):
    hdurl = response["hdurl"]
    return hdurl


def get_media_type(response):
    media_type = response["media_type"]
    return media_type


def get_title(response):
    title = response["title"]
    return title


def get_url(response):
    url = response["url"]
    return url

def get_date(response):
    date = response["date"]
    return date

def download_image(url, date, size:str):
    if os.path.isfile(f"{date}-{size}.jpg") == False:
        with urlopen(url) as response: 
            if response.status== 200:
                urlretrieve(url, f"{date}-{size}.jpg")
    else:
        return FileExistsError


# in theorie not needed. everything is already in jpg format. but just in case, we can convert the image to jpg
'''
def convert_image(image_path):
    path_to_image = os.path.normpath(image_path)

    basename = os.path.basename(path_to_image)

    filename_no_extension = basename.split(".")[0]

    base_directory = os.path.dirname(path_to_image)

    image = Image.open(path_to_image)
    image.save(f"{base_directory}/{filename_no_extension}.jpg", "JPEG")
'''