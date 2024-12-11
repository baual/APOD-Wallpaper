#Log management
from logging    import getLogger as lgGetLogger, \
    INFO, \
    basicConfig as lgBasicConfig

logger = lgGetLogger(__name__)
lgBasicConfig(
    format='%(filename)s - %(funcName)s - %(levelname)s: %(message)s',
    level=INFO
)


from datetime   import datetime,timezone

from os         import remove
from os.path    import isfile, getmtime, expanduser

"""Function that checks if there's a new APOD image available

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


apodPath = expanduser("~/.APOD.wallpaper.png")
print(checkAPOD(apodPath))
