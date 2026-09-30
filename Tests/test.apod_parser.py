import apod_parser.apod_object_parser as apod_parser
import json

from datetime import datetime

date = datetime.now().strftime("%y%m%d")
response = apod_parser.get_data(date)

print(json.dumps(response, indent=4, ensure_ascii=False))

print("explanaition: " + apod_parser.get_explaination(response))

print("url: " + apod_parser.get_url(response))

print("hdurl: " + apod_parser.get_hdurl(response))

print("get media type: " + apod_parser.get_media_type(response))

print("get title: " + apod_parser.get_title(response))

print("get date: " + apod_parser.get_date(response))

apod_parser.download_image(apod_parser.get_url(response), apod_parser.get_date(response), "small")

apod_parser.download_image(apod_parser.get_hdurl(response), apod_parser.get_date(response), "large")