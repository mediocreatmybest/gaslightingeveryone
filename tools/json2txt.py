import json
import os
import re
import argparse
import pathlib
import platform

from configparser import ConfigParser
from pathlib import Path
from func import json_extract, list2String # Local function script
from tqdm import tqdm

# Create the arg parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--imagedir', type=str, help='Image directory to caption', metavar='c:\images', required=False)
# Add arguments to disable unwanted data
parser.add_argument('--disable-title', action='store_true', help='Set this option to disable Title', required=False)
parser.add_argument('--disable-desc', action='store_true', help='Set this option to disable Desc', required=False)
parser.add_argument('--disable-tags', action='store_true', help='Set this option to disable Tags', required=False)
parser.add_argument('--remove-hash', action='store_true', help='Set this option to filter hash symbol from tags', required=False)
parser.add_argument('--disable-exif', action='store_true', help='Set this option to disable exif data', required=False)
parser.add_argument('--append', action='store_true', help='Set this option to append the files instead of overwriting', required=False)

# Add debug option to help disable save and prints out useful variables
parser.add_argument('--debug', action='store_true', help='Disables Saving files, prints output locations', required=False)

# Parse the argument
cmd_args = parser.parse_args()
# Create ConfigParser
config_parser = ConfigParser()
# Get the scripts parent directory so we can locate the config file
workingdir = Path(__file__).parent
# Name of working config file
# *Todo: * Switch this to a list, just because
configfile = 'config.ini'
# Join the working parent directory with the config file
workingconfig = pathlib.Path.joinpath(workingdir, configfile)
# read config file
read_files = config_parser.read(workingconfig)
# Sets the config file as a fallback directory
if cmd_args.imagedir is None:
    cmd_args.imagedir = config_parser.get('global', 'directory')
# Sets the Image and json directory from arguemnts
# Warning: this deletes the previous caption file

image_captions_path = Path(rf"{cmd_args.imagedir}")
image_captions_appended_file = "appended_captions.txt"
seperator = ", "

for root, dirs, files in os.walk(image_captions_path):
    for file in tqdm(files, desc="Creating txt files", unit="json2txts"):
        if file.endswith(".json"):
            jsonfile = (os.path.join(root, file))
            image_captions_single_file_base_dir = (os.path.join(root))
            # remove 1st extension
            image_captions_single_file_base_name = (os.path.splitext(file)[0])
            # remove the 2nd extension, better way to do this?
            image_captions_single_file = (os.path.splitext(image_captions_single_file_base_name)[0])

            # load json file from os.walk search
            with open(jsonfile, "r", encoding='UTF-8' ) as json_read:
            # returns JSON object as list or dictionary
                data = json.load(json_read)

            # Define our json search with json_extract function
            iso = json_extract(data, 'iso')
            focal_length = json_extract(data, 'focal_length')
            model = json_extract(data, 'model')
            aperture = json_extract(data, 'aperture')
            shutter_speed = json_extract(data, 'shutter_speed')

            # Cludge json data together even if it isn't listed as exif
            # Check if value actually has useful data, there has to be a better way to do this...
            cludge_camera_data = []
            if iso:
                cludge_iso = "ISO: " + str(iso[0])
                if cludge_iso != "ISO: ":
                    cludge_camera_data.append(cludge_iso)
            if focal_length:
                cludge_focal_length = "Focal Length: " + str(focal_length[0])
                if cludge_focal_length != "Focal Length: ":
                    cludge_camera_data.append(cludge_focal_length)
            if model:
                cludge_model = "Model is " + str(model[0])
                if cludge_model != "Model is ":
                    cludge_camera_data.append(cludge_model)
            if aperture:
                cludge_aperture = "Aperture: " + str(aperture[0])
                if cludge_aperture != "Aperture: ":
                    cludge_camera_data.append(cludge_aperture)
            if shutter_speed:
                cludge_shutter = "Shutter speed: " +str(shutter_speed[0])
                if cludge_shutter != "Shutter speed: ":
                    cludge_camera_data.append(cludge_shutter)

            # Some basic checks if data exists in json data that we don't want to search for via nested search
            # Assign json category to variable, hopefully this makes it easier to select known json data structures.
            if "category" in data:
                json_category = (data['category'])
            else:
                json_category = ""
            # Global fields
            if "title" in data:
                title = (data['title'])
            else:
                title = ""
            if "description" in data:
                desc = (data['description'])
            else:
                desc = ""
            if "tags" in data:
                tags = (data['tags'])
            else:
                tags = ""
            if "location" in data:
                locationlist = []
                city = json_extract(data, 'city')
                country = json_extract(data, 'country')
                for val in city:
                    if val != None :
                        locationlist.append(val)
                for val in country:
                    if val != None :
                        locationlist.append(val)
                location = list2String(locationlist)
            else:
                location = ""
            if "username" in data:
                username = (data['username'])
            else:
                username = ""
            # Reddit
            if "subreddit_name_prefixed" in data:
                subreddit = str(data['subreddit_name_prefixed'])
            else:
                subreddit = ""
            #Deviantart
            if "da_category" in data:
                da_category = (data['da_category'])
            else:
                da_category = ""
            # Artstation
            if json_category == "artstation":
                #as_full_name = json_extract(data, 'full_name')
                as_full_name = data['user']['full_name']
                as_username = json_extract(data, 'username')
                as_software = []
                as_software_list = data['software_items']
                for idx in as_software_list:
                    as_software.append(idx['name'])
                as_categories = []
                as_categories_list = (data['categories'])
                for idx in as_categories_list:
                    as_categories.append(idx['name'])
                as_mediums = []
                as_mediums_list = (data['mediums'])
                for idx in as_mediums_list:
                    as_mediums.append(idx['name'])

            else:
                as_full_name = ""
                as_username = ""
                as_software = ""
                as_categories = ""
                as_mediums = ""

            # Catch null or nothing values before it gets passed to regex
            if desc is None:
                desc = ""
            if title is None:
                title = ""

            # Clear data if command line data if flagged as disabled
            if cmd_args.disable_exif is True:
                cludge_camera_data = []
            if cmd_args.disable_title is True:
                title = ""
            if cmd_args.disable_desc is True:
                desc = ""
            if cmd_args.disable_tags is True:
                tags = ""

            # Simple filtering, move me somewhere else...
            # Remove text, html href links, and new lines
            exclusionList = ['<.*>','^^','www.','.com','.org','.net','http://','https://','|','&nbsp;','&amp','&gt','"','PROCESS INFO','SOURCE INFO','IMAGE INFO','\n']
            #exclusionList = ''
            exclusions = '|'.join(exclusionList)
            desc = re.sub(exclusions, '', desc)
            title = re.sub(exclusions, '', title)
            # Some additional HTML tags and move some symbols around
            desc = re.sub(r';', ', ', desc)
            title = re.sub(r';', ', ', title)
            # remove explicit :wiki: word, unable to get this to work any other way
            desc = re.sub(r'\:wiki\:', ' ', desc)
            title = re.sub(r'\:wiki\:', ' ', title)
            # remove triple and double dots
            desc = re.sub(r'\.\.\.', ' ', desc)
            title = re.sub(r'\.\.\.', ' ', title)
            desc = re.sub(r'\.\.', ' ', desc)
            title = re.sub(r'\.\.', ' ', title)
            # Change any " ~ " to simple space
            desc = re.sub(r' ~ ', ' ', desc)
            title = re.sub(r' ~ ', ' ', title)
            # Change any " - " to simple space
            desc = re.sub(r' - ', ' ', desc)
            title = re.sub(r' - ', ' ', title)
            # remove some additional symbols
            desc = re.sub(r'[\[\]\#!~?\=\(\)*.:-]', '', desc)
            title = re.sub(r'[\[\]\#!~?\=\(\)*.:-]', '', title)
            # If we leave behind any double spaces, change them to single space.
            desc = re.sub(r', , ', ', ', desc)
            title = re.sub(r', , ', ', ', title)
            desc = re.sub(r'  ', ' ', desc)
            title = re.sub(r'  ', ' ', title)
            desc = re.sub(r'   ', ' ', desc)
            title = re.sub(r'   ', ' ', title)
            # Final removal of all non-standard characters that break strings being selected, uncomment if needed.
            # desc = re.sub(r"[^-/().&' \w]|_", '', desc)
            # title = re.sub(r"[^-/().&' \w]|_", '', title)

            # move string into new variable to get camera cludge into output
            final_cludge_camera_data = list2String(cludge_camera_data)

            # move string into new variable to get tags into output
            final_tags_string = list2String(tags)

            # filter hash symbol if flagged in command arg
            if cmd_args.remove_hash is True:
                final_tags_string = re.sub(r'#', '', final_tags_string)

            # move string into new variable to get name into output
            # final_as_full_name = as_full_name

            # Make it easier on final output, append only existing results to a list
            appended_output = []

            if title != "":
                appended_output.append(title.strip())

            if desc != "":
                appended_output.append(desc.strip())

            if location != "":
                appended_output.append(location.strip())

            if final_cludge_camera_data != "":
                appended_output.append(final_cludge_camera_data.strip())

            if subreddit != "":
                appended_output.append(subreddit.strip())

            if da_category != "":
                appended_output.append(da_category)

            if username != "":
                appended_output.append(username)

            # Artstation append

            # AS Software as a caption
            if as_software != "":
                as_software_str = 'Created with '
                as_software_str = as_software_str + list2String(as_software)
                appended_output.append(as_software_str)

            if len(as_categories):
                appended_output.append(list2String(as_categories))

            if len(as_mediums):
                appended_output.append(list2String(as_mediums))

            if as_full_name != "":
                appended_output.append(as_full_name)

            if as_username != "":
                appended_output.append(as_username[0])

            if tags != "":
                appended_output.append(final_tags_string.strip())

            return_appended_output = list2String(appended_output)

            # Trailing comma, please leave.
            return_appended_output = return_appended_output.strip(', ')

            # Quick fix to work if platform.system() == "Windows":out directory seperators, please switch me to path
            if platform.system() == "Windows":
                pathsep = "\\"
            else:
                pathsep = "/"

            # Folder and File locations
            single_files = image_captions_single_file_base_dir + pathsep + image_captions_single_file + ".txt"
            appended_file = str(image_captions_path) + pathsep + image_captions_appended_file
            # Appended file contents
            appended_contents = image_captions_single_file_base_dir + pathsep + image_captions_single_file_base_name + seperator + return_appended_output + "\n"

            # Debug print file name and locations
            if cmd_args.debug is True:
                print(single_files)
                print(appended_contents)

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

            # Create new file and overwrite if exists
            if savefiles is True:
                with open(single_files, f'{writeflag}', encoding='UTF-8') as f:
                    f.write(return_appended_output)

                with open(appended_file, 'a', encoding='UTF-8') as fa:
                    fa.write(appended_contents)