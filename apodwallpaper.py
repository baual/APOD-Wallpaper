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
from urllib3 import PoolManager

def internet_conn() -> bool:
    logger.info("Checking internet connectivity")
    http = PoolManager(timeout=3.0)
    r = http.request('GET', 'google.com', preload_content=False)
    code = r.status
    r.release_conn()
    if code == 200:
        return True
    else:
        return False
        logger.error("No internet connectivity")
    
#print(check_internet_conn())


"""
getAPOD() 

Function that gets the APOD url using the NASA API

Return value (str)
------------------
APOD URL - URL retrieved successfully
None     - Error

"""

from requests   import get as reqGet

def getAPOD() -> str:
    logger.info("Downloading APOD image URL")
    # Used DEMO_KEY as the api_key since the constraints are based on IP
    response = reqGet('https://api.nasa.gov/planetary/apod',
                      params={
                          'api_key' : 'DEMO_KEY'
                      })
    # Status code check
    if response.status_code == 200:
        logger.info("Download successful")
        information = response.json()
        if information.get('media_type') == "image":
            url = response.json()['hdurl']
            isphoto = True
        elif information.get('media_type') == "video":
            url = response.json()['url']
            isphoto = False
        else:
            raise RuntimeError("APOD is not an image or video")
    else:
        logger.error("Can't get the APOD image URL")
        logger.error("Status code: %s", response.status_code)
    return (isphoto, url, response.json()['title'])


#print(getAPOD())



"""
la fin

"""
"""
from os.path    import expanduser

def main():
    logger.info("Init script")
    # Path to APOD image on local storage
    apodPath = expanduser("~/.wallpaper.png")
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

"""