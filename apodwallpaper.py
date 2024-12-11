#Log management
from logging    import getLogger as lgGetLogger, \
    INFO, \
    basicConfig as lgBasicConfig

logger = lgGetLogger(__name__)
lgBasicConfig(
    format='%(filename)s - %(funcName)s - %(levelname)s: %(message)s',
    level=INFO
)

#imports
from urllib import error
from urllib.request import urlopen, urlretrieve

import json

from datetime   import datetime, timezone

from os         import remove
from os.path    import isfile, getmtime, dirname, abspath, expanduser

from subprocess import run as subRun, DEVNULL as subDevNull



"""
internet_conn()

Function that checks if there's internet connectivity 

Return value (boolean)
------------------
True - connection internet
False - pas de connection

"""
def internet_conn() -> bool:
    logger.info("Checking internet connectivity")
    try:
        urlopen("https://www.google.com")
        return True
    except error.URLError:
        return False
        logger.error("No internet connectivity")
    
# print(internet_conn())


"""
getAPOD() 

Function that gets the APOD url using the NASA API

Return value (str)
------------------
APOD URL - URL retrieved successfully
None     - Error

"""
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


"""Function that checks if there's a new APOD image available
checkAPOD(apodPath)

Parameters
----------
apodPath : str - Path to the apod-image

Return value (int)
------------------
0 - The image is up-to-date
1 - New image available

"""
def checkAPOD(apodPath) -> int:
    logger.info("Checking if image need to be updated")
    res = 1
    if isfile(apodPath):
        # File exists
        #obsolete
        #lastModDay = datetime.utcfromtimestamp(
        #    getmtime(apodPath)).strftime("%Y/%m/%d")
        #today = datetime.utcnow().strftime("%Y/%m/%d")
        lastModDay =datetime.fromtimestamp(getmtime(apodPath)).replace(tzinfo=timezone.utc).strftime("%Y/%m/%d")
        today = datetime.now().replace(tzinfo=timezone.utc).strftime("%Y/%m/%d")  
        if lastModDay == today:
            logger.info("Image up-to-date")
            res = 0
        else:
            # New APOD available => download
            logger.info("New image available")
    else:
        # File doesn't exists => download
        logger.info("No image found")
    return res






"""Function that shows the user of the APOD name

Parameters
----------
apodName : str - Name of the APOD

Return value (int)
------------------
0    - User notified successfully
None - Error

"""
def apodNotify(apodName) -> int:
    # Run notify-send with custom params and the name of the APOD image
    res = subRun(
        ['notify-send',
         '-u', 'low',
         '-t', '10000',
         '-a', 'APOD-Wallpaper',
         apodName]).returncode
    # Check return code to print error message
    if res != 0:
        logger.error("notify-send failed")
        logger.error("Status code: %s", res)
    return res


"""Function that sets the backgroud/wallpaper using feh
setWallpaper(apodPath)

Parameters
----------
apodPath : str - Path to the apod-image.png on the users' computer

Return value (int)
------------------
0    - Image set successfully
None - Error

"""
def setWallpaper(apodPath) -> int:
    logger.info("Running feh")
    # Run feh command using the photo local path
    res = subRun(
        ['feh', '--no-fehbg', '--bg-scale', apodPath]
    ).returncode
    # Check return code to print error message
    if res != 0:
        logger.error("feh failed")
        logger.error("Status code: %s", res)
    return res


"""Function used to download the new APOD image, replacing the older one
downloadAPOD(apodURL, apodPath, apodIsImage)

Parameters
----------
apodURL  : str - URL of todays' APOd image
apodPath : str - Path to the apod-image on the users' computer
apodIsImage : bool - True if file is an image


Return value (int)
------------------
0 - The new APOD image has been downloaded successfully
1 - Error

"""
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


def main():
    logger.info("Init script")
    # Path to APOD image on local storage
    apodPath = expanduser("~/.APOD.wallpaper.png")
    # Check if new APOD image available
    if checkAPOD(apodPath) != 0:
        if not internet_conn():
            exit(1)
            # Get APOD URL
        apodIsImage, apodURL, apodTitle  = getAPOD()
        if apodURL is None:
            exit(2)
            # Download image
        if downloadAPOD(apodURL, apodPath, apodIsImage) != 0:
            exit(3)
        if apodNotify(apodTitle) != 0:
            exit(4)
            # Set APOD image
    setWallpaper(apodPath)
    exit(0)


if __name__ == "__main__":
    main()
