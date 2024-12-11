#test API KEY

from urllib.request import Request, urlopen
import json

def getAPOD() -> dict:

    my_url = "https://api.nasa.gov/planetary/apod"
    my_header="api_key=DEMO_KEY"
    with urlopen(my_url+"?"+my_header) as response: 
        print(response.status)
        body = response.read()
    #Request ne marche pas car HTTP seulement
    #my_headers = { "api_key" : "DEMO_KEY" }
    #req=Request(url=my_url,headers=my_headers)
    #with urlopen(req) as response: body = response.read()

    #todo_item= json.loads(body)
    #print(type(todo_item))
    #print(todo_item)

    return json.loads(body)

print(getAPOD())