import json
import requests

with open("jsonHub.json", 'w+') as file:
    req = requests.get('https://api.github.com/users/ZSUNSET/repos')
    for i in req.json():
        file.write(json.dumps(i))
