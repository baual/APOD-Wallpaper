#Log management
from logging    import getLogger as lgGetLogger, \
    INFO, \
    basicConfig as lgBasicConfig

logger = lgGetLogger(__name__)
lgBasicConfig(
    format='%(filename)s - %(funcName)s - %(levelname)s: %(message)s',
    level=INFO
)



"""Function that checks if there's internet connectivity 

Return value (boolean)
------------------
True - connection internet
False - pas de connection

"""
from urllib import error
from urllib.request import urlopen, urlretrieve

def internet_conn() -> bool:
    logger.info("Checking internet connectivity")
    try:
        urlopen("https://www.google.com")
        return True
    except error.URLError:
        return False
        logger.error("No internet connectivity")
    
print(internet_conn())


"""
getAPOD() 

Function that gets the APOD url using the NASA API

Return value (str)
------------------
APOD URL - URL retrieved successfully
None     - Error

"""

import json

def getAPOD() -> str:
    logger.info("Downloading APOD image URL")
    # Used DEMO_KEY as the api_key since the constraints are based on IP
    my_url = "https://api.nasa.gov/planetary/apod"
    my_header="api_key=DEMO_KEY"
    with urlopen(my_url+"?"+my_header) as response: 
    # Status code check
        if response.status == 200:
            logger.info("Download successful")
            information = json.loads(response.read())
            if information.get('media_type') == "image":
                url = information['hdurl']
                isphoto = True
            elif information.get('media_type') == "video":
                url = information['url']
                isphoto = False
            else:
                raise RuntimeError("APOD is not an image or video")
        else:
            logger.error("Can't get the APOD image URL")
            logger.error("Status code: %s", response.status)
    return (isphoto, url, information['title'])


def downloadAPOD(apodURL, apodPath, apodIsImage) -> int:
    result = 0
    # Download APOD image
    if apodIsImage:
        logger.info("Downloading APOD image")
        with urlopen(apodURL) as response: 
            if response.status== 200:
                # Write new image (overwriting the older one)
                urlretrieve(apodURL,apodPath)
            else:
                # Error occurred => Print error messages
                result = 1
                logger.error("Download of APOD image failed")
                logger.error("Status code: %s", response.status )
    else:
        logger.info("No video allowed")
        result = 1
    return result

from os.path    import expanduser

apodIsImage, apodURL, apodTitle  = getAPOD()

apodPath = expanduser("~/.APOD.wallpaper.png")

if apodURL is None:
    exit(2)
    # Download image
if downloadAPOD(apodURL, apodPath, apodIsImage) != 0:
    exit(3)
