#Log management
from logging    import getLogger as lgGetLogger, \
    INFO, \
    basicConfig as lgBasicConfig

logger = lgGetLogger(__name__)
lgBasicConfig(
    format='%(filename)s - %(funcName)s - %(levelname)s: %(message)s',
    level=INFO
)



import urllib.request

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


print(getAPOD())

