import json
import os
import argparse
import requests

from pathlib import Path

# Python script for plant net ID
# This script may help adding common names and scientific names to caption text files
# An API account is required, a free account allows up to 500 API calls per day

# Set allowed images for directory scan
image_filter = ('.png', '.jpg', '.jpeg')

# Create the arg parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--imagedir', type=str, help='Image directory of plants to ID', metavar='c:\images', required=True)
parser.add_argument('--apikey', type=str, help='API Key from my.plantnet.org', metavar='12345abcd', required=True)
parser.add_argument('--append', action='store_true', help='Set this option to append the files instead of overwriting', required=False)
parser.add_argument('--debug', action='store_true', help='Debug will disable sending images or saving files', required=False)
parser.add_argument('--dump-json', action='store_true', help='Set this option to save the json file', required=False)

# Parse the argument
cmd_args = parser.parse_args()
# Set caption path from command arguments
image_captions_path = Path(rf"{cmd_args.imagedir}")
API_KEY = cmd_args.apikey

# Set image data for API, valid options are: leaf, flower, fruit, bark, auto. Lets go with automagic.
image_data = {'organs': ['auto']}

# Debug
if cmd_args.debug is True:
    print('Image data to be sent with image: ', image_data)

# Set API project and api_key endpoint
PROJECT = "all" # try "weurope" or "canada"
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

# Debug
if cmd_args.debug is True:
    print('API Key: ', API_KEY)
    print('Project area selected is: ', PROJECT)
    print('The API URL being called is: ', api_endpoint)

for root, dirs, imgfiles in os.walk(image_captions_path):
    for image_file in imgfiles:
        # Use casefold() or lower() to make it a (case) insensitive jerk
        if image_file.casefold().endswith(image_filter):
            image_path = (os.path.join(root))
            full_image_path = os.path.join(image_path, image_file)
            # remove extension so we can create a text file from image name
            file_base_name = (os.path.splitext(full_image_path)[0])
            # Set caption and json file
            caption_file = file_base_name + '.txt'
            json_file = file_base_name + '.json'


            # Debug
            if cmd_args.debug is True:
                print('Full image path to file is: ', full_image_path)
                print('Full image path and base file name is: ', file_base_name)
                print('Full image path and caption file is: ', caption_file)

            # Open file as read in binary, rb.
            open_image = open(full_image_path, 'rb')

            image_file_w_data = [('images', (full_image_path, open_image))]

            # Debug
            if cmd_args.debug is True:
                print('Image and data being pushed to API: ', image_file_w_data)

            req = requests.Request('POST', url=api_endpoint, files=image_file_w_data, data=image_data)

            prepared = req.prepare()

            s = requests.Session()
            response = s.send(prepared)
            json_result = json.loads(response.text)

            # Selecting only the first and best result. The best match and Scientific name should match
            best_match = json_result['bestMatch']
            match_score =  json_result['results'][0]['score']
            common_name = json_result['results'][0]['species']['commonNames'][0]
            scientific_name = json_result['results'][0]['species']['scientificName']

            data_content = f'a {common_name}, also called {scientific_name}'
            data_content_append = f', a {common_name}, also called {scientific_name}'

            # Debug
            if cmd_args.debug is True:
                print('The best match is: ', best_match)
                print('The common name is: ', common_name)
                print('The scientific name is: ', scientific_name)
                print('The quality match score out of 100 is: ', match_score)
                if best_match == scientific_name:
                    print('Best match and scientific name match.')
                else:
                    print('Best match and scientific name do not match.')


            # Close the file I guess.
            open_image.close

            # Check if debug is enabled to disable saving
            if cmd_args.debug is True:
                savefiles = False
            else:
                savefiles = True

            # Set write flag to overwrite
            writeflag = 'w'

            # Set append if cmd is flagged
            if cmd_args.append is True:
                writeflag = 'a'

            if cmd_args.debug is True:
                print('writeflag is: ', writeflag)

            # Create new file and or overwrite if exists
            if savefiles is True and writeflag == 'w':
                with open(caption_file, f'{writeflag}', encoding='utf-8') as f:
                    f.write(data_content)
                    f.close

            # Create new file and or append
            if savefiles is True and writeflag == 'a':
                with open(caption_file, f'{writeflag}', encoding='utf-8') as f:
                    f.write(data_content_append)
                    f.close

            # Create new file and or overwrite if exists
            if savefiles is True and cmd_args.dump_json is True:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(json_result, f)
                    f.close