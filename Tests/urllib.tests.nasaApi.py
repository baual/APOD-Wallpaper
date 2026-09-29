from urllib.request import Request, urlopen
import json
from datetime import datetime

def getAPOD(date) -> dict:

    with urlopen(f"https://science.nasa.gov/wp-json/wp/v2/apod-basic/{date}") as response:
        print(response.status)
        body = json.load(response)

    return body

date = datetime.now().strftime("%y%m%d")
response = getAPOD(date)
print(json.dumps(response, indent=4, ensure_ascii=False))

