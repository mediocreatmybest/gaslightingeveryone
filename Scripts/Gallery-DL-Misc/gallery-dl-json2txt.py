import json
import os
import re
from pathlib import Path

#image and json directory
image_captions_path = Path(r"c:\test")
image_captions_appended_file = "appended_captions.txt" 

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

            #fields from json file we are intrested in. 
            title = (data['title'])
            desc = (data['description'])
            tags = (data['tags'])

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
            desc = re.sub(r'[!~?\=\(\)*.:-]', '', desc)
            title = re.sub(r'[!~?\=\(\)*.:-]', '', title)
            #If we leave behind any double spaces, change them to single space.
            desc = re.sub(r'  ', ' ', desc)
            title = re.sub(r'  ', ' ', title)
            #Change any " - " to simple space
            desc = re.sub(r' - ', ' ', desc)
            title = re.sub(r' - ', ' ', title)

            #Convert tags into string

            # Function to convert 
            def listToString(tags):
   
             # initialize a seperator string
                seperator = ", "
            # return string 
                return (seperator.join(tags))
       
            #move string into new variable to get tags into output
            final_tags_string = (listToString(tags))

            #Moving strings into final output string and strip blank space at start and end, (title,desc,tags)
            final_result = title.strip() + ", " + desc.strip() + ", " + final_tags_string.strip()

            #Output to console? All of it or just some? uncomment
            #print(final_result)
            #print(title)
            #print(desc)
            #print(final_tags_string)

            #Seperator for output
            seperator = ", "

            #Folder and File locations
            single_files = image_captions_single_file_base_dir + "\\" + image_captions_single_file + ".txt"
            #print (image_captions_single_file, seperator, single_files)
            appended_file = str(image_captions_path) + "\\" + image_captions_appended_file
            #print(appended_file)
            #Appended file contents 
            appended_contents = image_captions_single_file_base_dir + "\\" + image_captions_single_file + seperator + final_result + "\n"
            #print (appended_contents)
            #Create new file and overwrite if exists

            with open(single_files, 'w') as f:
                f.write(final_result)
                f.close
    
            with open(appended_file, 'a') as fa:
                fa.write(appended_contents)
                fa.close
             


             
             
