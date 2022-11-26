import json
import os
import re
from pathlib import Path

#image and json directory
image_captions_path = Path(r"c:\images")
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
            with open(jsonfile, "r") as json_read:
            # returns JSON object as list or dictionary
                data = json.load(json_read)

            #Function to extract nested json data, 
            #https://hackersandslackers.com/extract-data-from-complex-json-python/
            def json_extract(obj, key):
                #Recursively fetch values from nested JSON.
                arr = []

                def extract(obj, arr, key):
                    #Recursively search for values of key in JSON tree.
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

            #print (cludge_camera_data)

            

            #fields from json file we are intrested in, with some basic error checks
            #exif is nested, we are only looking for specific single fields, how many extractors have exif? 
            #if "exif" in data:
                #exif_aperture = str(data['exif']['aperture'])
            #    exif_aperture = json_extract(data, 'aperture')
                #exif_focal = str(data['exif']['focal_length']) 
            #    exif_focal = json_extract(data, 'focal_length')
                #exif_iso = str(data['exif']['iso'])
            #    exif_iso = json_extract(data, 'iso')
                #exif_model = str(data['exif']['model'])
            #    exif_model = json_extract(data, 'model')
                #exif_collected = "Image created with " + "an aperture of " + exif_aperture[0] + seperator + "focal length of " + exif_focal[0] + seperator + "with an ISO of " + exif_iso[0] + seperator + "Model is " + exif_model[0]
            #else:
            #    exif = ""
            #    exif_collected = ""
            
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
            if "subreddit_name_prefixed" in data:
                subreddit = (data['subreddit_name_prefixed'])
            else: subreddit = ""
            if "location" in data:
                location = (data['location'])
            else:
                location = ""

            

            # Simple filtering
            # Remove text, html href links, and new lines 
            exclusionList = ['PROCESS INFO','SOURCE INFO','IMAGE INFO','<a.*</a>','\n']
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
            desc = re.sub(r'[\#!~?\=\(\)*.:-]', '', desc)
            title = re.sub(r'[\#!~?\=\(\)*.:-]', '', title)
            #If we leave behind any double spaces, change them to single space.
            desc = re.sub(r'  ', ' ', desc)
            title = re.sub(r'  ', ' ', title)

            
            #Function to convert tags to string
            def listToString(cludge_camera_data):
                #initialize a seperator string
                seperator = ", "
                #return string 
                return (seperator.join(cludge_camera_data))
            
            #move string into new variable to get tags into output
            final_cludge_camera_data = (listToString(cludge_camera_data))
            #Moving strings into final output string and strip blank space at start and end, (title,desc,tags)
            #final_result = title.strip() + ", " + desc.strip() + ", " + final_tags_string.strip()

            #Function to convert tags to string
            def listToString(tags):
                #initialize a seperator string
                seperator = ", "
                #return string 
                return (seperator.join(tags))
            
            #move string into new variable to get tags into output
            final_tags_string = (listToString(tags))

            #Output to console? All of it or just some? uncomment
            #print(final_result)
            #print(title)
            #print(desc)
            #print(final_tags_string)
            #print(exif_collected)
            
            #Make it easier on final output, append only existing results to a list

            appended_output = []
            
            if title != "":
                appended_output.append(title.strip())

            if desc != "":
                appended_output.append(desc.strip())

            if final_cludge_camera_data != "":
                appended_output.append(final_cludge_camera_data.strip())

            if subreddit != "":
                appended_output.append(subreddit.strip())

            if tags != "":
                appended_output.append(final_tags_string.strip())
                
            print(appended_output)
    
            #Function to convert list to string with seperator
            def listToString(appended_output):
                #initialize a seperator string
                seperator = ", "
                #return string 
                return (seperator.join(appended_output))
            
            return_appended_output = (listToString(appended_output))
            
            #print(return_appended_output)

            #Seperator for output
            seperator = ", "
            #Folder and File locations
            single_files = image_captions_single_file_base_dir + "\\" + image_captions_single_file + ".txt"
            appended_file = str(image_captions_path) + "\\" + image_captions_appended_file
            #Appended file contents 
            appended_contents = image_captions_single_file_base_dir + "\\" + image_captions_single_file + seperator + return_appended_output + "\n"

            #Create new file and overwrite if exists
            with open(single_files, 'w') as f:
                f.write(return_appended_output)
                f.close
    

            with open(appended_file, 'a') as fa:
                fa.write(appended_contents)
                fa.close