import json
import requests #install via pip
from pprint import pprint

API_KEY = "1234567890"  # Set you API_KEY here
PROJECT = "all" # try "weurope" or "canada"
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"


image_path_1 = "C:\\images\\plants\\Flame.jpg"
image_data_1 = open(image_path_1, 'rb')

data = {'organs': ['auto']}

files = [('images', (image_path_1, image_data_1))]

req = requests.Request('POST', url=api_endpoint, files=files, data=data)
prepared = req.prepare()

s = requests.Session()
response = s.send(prepared)
json_result = json.loads(response.text)

pprint(response.status_code)
pprint(json_result)
