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

            #fields from json file we are intrested in, with some basic error checks
            #exif is nested, we are only looking for specific single fields, how many extractors have exif? 
            if "exif" in data:
                exif_aperture = str(data['exif']['aperture'])
                exif_focal = str(data['exif']['focal_length']) 
                exif_iso = str(data['exif']['iso'])
                exif_model = str(data['exif']['model'])
                exif_collected = "Image created with " + "an aperture of " + exif_aperture + seperator + "focal length of " + exif_focal + seperator + "with an ISO of " + exif_iso + seperator + "Model is " + exif_model
            else:
                exif = ""
                exif_aperture = ""
                exif_focal = ""
                exif_iso = ""
                exif_model = ""
                exif_collected = ""
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
            #remove some additional symbols
            desc = re.sub(r'[\#!~?\=\(\)*.:-]', '', desc)
            title = re.sub(r'[\#!~?\=\(\)*.:-]', '', title)
            #If we leave behind any double spaces, change them to single space.
            desc = re.sub(r'  ', ' ', desc)
            title = re.sub(r'  ', ' ', title)
            #Change any " - " to simple space
            desc = re.sub(r' - ', ' ', desc)
            title = re.sub(r' - ', ' ', title)

            
            #Function to convert tags to string
            def listToString(tags):
                #initialize a seperator string
                seperator = ", "
                #return string 
                return (seperator.join(tags))
                   
            #Function to extract nested json, 
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
     
            #iso = json_extract(data, 'iso')
            #print(iso)
            
            #move string into new variable to get tags into output
            final_tags_string = (listToString(tags))
            #Moving strings into final output string and strip blank space at start and end, (title,desc,tags)
            final_result = title.strip() + ", " + desc.strip() + ", " + final_tags_string.strip()

            #Output to console? All of it or just some? uncomment
            #print(final_result)
            #print(title)
            #print(desc)
            #print(final_tags_string)
            #print(exif_collected)

            
            #Seperator for output
            seperator = ", "
            #Folder and File locations
            single_files = image_captions_single_file_base_dir + "\\" + image_captions_single_file + ".txt"
            appended_file = str(image_captions_path) + "\\" + image_captions_appended_file
            #Appended file contents 
            appended_contents = image_captions_single_file_base_dir + "\\" + image_captions_single_file + seperator + final_result + "\n"
            
            
            #exif_data = []
            #if exif_iso not in exif_data:
            #    print(exif_data)
            #    exif_data.append(exif_iso)
            #    print(exif_data)
            
            #Create new file and overwrite if exists
            #with open(single_files, 'w') as f:
            #    f.write(final_result)
            #    f.close
    
            #with open(appended_file, 'a') as fa:
            #    fa.write(appended_contents)
            #    fa.close