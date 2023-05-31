import requests
import json

start_date = '2020-02-16'
end_date = '2020-02-11'
token = 'tHWpu6rXLlFFparhl59wsGpADBUdE7hnEIdHrfE4'
req = requests.get(
    f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={token}')


with open('cosmic.json', 'w+') as file:
    file.write(json.dumps(req.json()))
