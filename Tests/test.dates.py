from datetime import datetime, timezone
from os.path    import getmtime, expanduser

apodPath = expanduser("~/.APOD.wallpaper.png")

#obsolete
#lastModDay = datetime.utcfromtimestamp(
#    getmtime(apodPath)).strftime("%Y/%m/%d")
#today = datetime.utcnow().strftime("%Y/%m/%d")

#lastModDay = datetime.fromtimestamp(datetime.timezone.utc(getmtime(apodPath)).strftime("%Y/%m/%d"))
today = datetime.now()
todayutc=today.replace(tzinfo=timezone.utc).strftime("%Y/%m/%d")
print(today.strftime("%Y/%m/%d"))
print(todayutc)

lastModDay =datetime.fromtimestamp(getmtime(apodPath)).replace(tzinfo=timezone.utc).strftime("%Y/%m/%d")
print(lastModDay)