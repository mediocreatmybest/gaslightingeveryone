import json
import os
import argparse
import requests # Need to install with pip or other
#from pprint import pprint

from pathlib import Path

# Set allowed images for directory scan
image_filter = ('.png', '.jpg', '.jpeg')

# Create the arg parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--imagedir', type=str, help='Image directory of plants to ID', metavar='c:\images', required=True)
parser.add_argument('--apikey', type=str, help='API Key from my.plantnet.org', metavar='12345abcd', required=True)
parser.add_argument('--debug', action='store_true', help='Debug will disable sending images or saving files', required=False)

# Parse the argument
cmd_args = parser.parse_args()
# Set caption path from command arguments
image_captions_path = Path(rf"{cmd_args.imagedir}")
API_KEY = cmd_args.apikey

# Set image data for API, valid options are: leaf, flower, fruit, bark, auto. Lets go with automagic.
image_data = {'organs': ['auto']}

# Set API project and api_key endpoint
PROJECT = "all" # try "weurope" or "canada"
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

for root, dirs, imgfiles in os.walk(image_captions_path):
    for image_file in imgfiles:
        # Use casefold() or lower() to make it a (case) insensitive jerk
        if image_file.casefold().endswith(image_filter):
            image_path = (os.path.join(root))
            full_image_path = os.path.join(image_path, image_file)

            # Open file as read in binary, rb. 
            open_image = open(full_image_path, 'rb')

            image_file_w_data = [('images', (full_image_path, open_image))]

            req = requests.Request('POST', url=api_endpoint, files=image_file_w_data, data=image_data)

            prepared = req.prepare()

            s = requests.Session()
            response = s.send(prepared)
            json_result = json.loads(response.text)

            best_match = json_result['bestMatch']
            match_score =  json_result['results'][0]['score']
            common_name = json_result['results'][0]['species']['commonNames'][0]
            scientific_name = json_result['results'][0]['species']['scientificName']
            
            print('The best match is: ', best_match)
            print('The common name is: ', common_name)
            print('The scientific name is: ', scientific_name)
            print('The quality match score out of 100 is: ', match_score)

            # Close  the file I guess. 
            open_image.close

            
            #with open('data.json', 'w') as f:
            #    json.dump(json_result, f)

            #pprint(response.status_code)
            #pprint(json_result)
            #print(json_result)













