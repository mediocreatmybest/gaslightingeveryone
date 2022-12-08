import json
import os
import re
import sys
#import codecs #Will we need this later...
from pathlib import Path

#image and json directory
# To do: not delete old caption data and back it up.
image_captions_path = Path(r"C:\images")
image_captions_appended_file = "appended_captions.txt"
seperator = ", "

for root, dirs, files in os.walk(image_captions_path):
    for file in files:
        if file.endswith(".json"):
            jsonfile = (os.path.join(root, file))
            image_captions_single_file_base_dir = (os.path.join(root))
            image_captions_single_file_base_name = (os.path.splitext(file)[0])
            image_captions_single_file = image_captions_single_file_base_name

            #load json file from os.walk search
            with open(jsonfile, "r", encoding='UTF-8' ) as json_read:
            # returns JSON object as list or dictionary
                data = json.load(json_read)

            # Function to extract nested json data
            # https://hackersandslackers.com/extract-data-from-complex-json-python
            def json_extract(obj, key):
                #Recursively fetch values from nested JSON.
                arr = []

                def extract(obj, arr, key):
                    # Recursively search for values of key in JSON tree
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if isinstance(v, (dict, list)):
                                extract(v, arr, key)
                            elif k == key:
                                arr.append(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            extract(item, arr, key)
                    return arr

                values = extract(obj, arr, key)
                return values

            #Extract nested json via function
            #print(json_extract(data, 'iso'))

            iso = json_extract(data, 'iso')
            focal_length = json_extract(data, 'focal_length')
            model = json_extract(data, 'model')
            aperture = json_extract(data, 'aperture')
            shutter_speed = json_extract(data, 'shutter_speed')

            #Cludge json data together even if it isn't listed as exif
            #Check if value actually has useful data, there has to be a better way to do this...
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
            #Global fields
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
                location = ""
                #location = str(data['location']) #why aren't these fields standardised? Am I so out of touch?... No it's the children that are wrong...
            else:
                location = ""
            if "username" in data:
                username = (data['username'])
            else:
                username = ""
            #Reddit
            if "subreddit_name_prefixed" in data:
                subreddit = str(data['subreddit_name_prefixed'])
            else:
                subreddit = ""
            #Deviantart
            if "da_category" in data:
                da_category = (data['da_category'])
            else:
                da_category = ""
            #Artstation
            if json_category == "artstation":
                as_data = json_extract(data, 'name')
                as_username = json_extract(data, 'username')
            else:
                as_data = ""
                as_username = ""

            #Catch null or nothing values before it gets passed to regex
            if desc is None:
                desc = ""
            if title is None:
                title = ""

            # Simple filtering
            # Remove text, html href links, and new lines
            exclusionList = ['www.','.com','.org','.net','http://','https://','<b>','</b>','PROCESS INFO','SOURCE INFO','IMAGE INFO','<a.*</a>','\n']
            exclusions = '|'.join(exclusionList)
            title = re.sub(exclusions, '', title)
            desc = re.sub(exclusions, '', desc)
            #remove explicit :wiki: word, unable to get this to work any other way
            desc = re.sub(r'\:wiki\:', ' ', desc)
            title = re.sub(r'\:wiki\:', ' ', title)
            #remove triple and double dots
            desc = re.sub(r'\.\.\.', ' ', desc)
            title = re.sub(r'\.\.\.', ' ', title)
            desc = re.sub(r'\.\.', ' ', desc)
            title = re.sub(r'\.\.', ' ', title)
            #Change any " ~ " to simple space
            desc = re.sub(r' ~ ', ' ', desc)
            title = re.sub(r' ~ ', ' ', title)
            #Change any " - " to simple space
            desc = re.sub(r' - ', ' ', desc)
            title = re.sub(r' - ', ' ', title)
            #remove some additional symbols
            desc = re.sub(r'[\[\]\#!~?\=\(\)*.:-]', '', desc)
            title = re.sub(r'[\[\]\#!~?\=\(\)*.:-]', '', title)
            #If we leave behind any double spaces, change them to single space.
            desc = re.sub(r'  ', ' ', desc)
            title = re.sub(r'  ', ' ', title)
            #Final removal of all non-standard characters that break strings being selected, uncomment if needed.
            #desc = re.sub(r"[^-/().&' \w]|_", '', desc)
            #title = re.sub(r"[^-/().&' \w]|_", '', title)
            #Function to convert cludged camera data to string
            def listToString(cludge_camera_data):
                #initialize a seperator string
                seperator = ", "
                #return string
                return (seperator.join(cludge_camera_data))

            #move string into new variable to get camera cludge into output
            final_cludge_camera_data = (listToString(cludge_camera_data))

            #Function to convert tags to string
            def listToString(tags):
                #initialize a seperator string
                seperator = ", "
                #return string
                return (seperator.join(tags))

            #move string into new variable to get tags into output
            final_tags_string = (listToString(tags))

                        #Function to convert tags to string
            def listToString(as_data):
                #initialize a seperator string
                seperator = ", "
                #return string
                return (seperator.join(as_data))

            #move string into new variable to get tags into output
            final_as_data = (listToString(as_data))

            #Make it easier on final output, append only existing results to a list
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

            if as_data != "":
                appended_output.append(final_as_data)

            if as_username != "":
                appended_output.append(as_username[0])

            if tags != "":
                appended_output.append(final_tags_string.strip())

            #Function to convert list to string with seperator
            def listToString(appended_output):
                #initialize a seperator string
                seperator = ", "
                #return string
                return (seperator.join(appended_output))

            return_appended_output = (listToString(appended_output))

            #Seperator for output
            seperator = ", "
            #Folder and File locations
            single_files = image_captions_single_file_base_dir + "\\" + image_captions_single_file + ".txt"
            appended_file = str(image_captions_path) + "\\" + image_captions_appended_file
            #Appended file contents
            appended_contents = image_captions_single_file_base_dir + "\\" + image_captions_single_file + seperator + return_appended_output + "\n"

            #Create new file and overwrite if exists
            with open(single_files, 'w', encoding='UTF-8') as f:
                f.write(return_appended_output)
                f.close

            with open(appended_file, 'a', encoding='UTF-8') as fa:
                fa.write(appended_contents)
                fa.close

           # with open(appended_file, 'a', encoding='UTF-8') as falog:
           #     falog.write(image_captions_single_file)
           #     falog.close