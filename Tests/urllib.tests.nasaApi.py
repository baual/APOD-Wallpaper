from urllib.request import urlopen
import json
url = "https://jsonplaceholder.typicode.com/todos/1"
with urlopen(url) as response:
    body = response.read()

todo_item = json.loads(body)
print(todo_item)


#test API KEY
from urllib.request import Request, urlopen
import json
#url = "https://api.nasa.gov/planetary/apod"
#req=Request(url)
#req.add_header('api_key','DEMO_KEY')
#with urlopen(req) as response:
url="https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
with urlopen(url) as response:


    body = response.read()

todo_item = json.loads(body)
print(todo_item)