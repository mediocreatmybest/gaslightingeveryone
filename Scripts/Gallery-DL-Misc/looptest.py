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
            image_captions_single_file_base = (os.path.join(root, file))
            image_captions_single_file = image_captions_single_file_base 
            
            
            
             
            #load json file from os.walk search 
            #jsonfile = open(r"c:\test\file1.jpg.json", "r")           
            print (jsonfile)
            with open(jsonfile, "r") as json_read:
            # returns JSON object as 
            # a dictionary or list
                data = json.load(json_read)

            
            title = (data['title'])
            desc = (data['description'])
            tags = (data['tags'])

            # Simple filtering
            # Remove set text, html href links, and new lines 
            exclusionList = ['PROCESS INFO','SOURCE INFO','IMAGE INFO','<a.*</a>','\n']
            exclusions = '|'.join(exclusionList)
            title = re.sub(exclusions, '', title)
            desc = re.sub(exclusions, '', desc)

            #remove explicit :wiki: word, unable to get this to work any other way
            desc = re.sub(r'\:wiki\:', ' ', desc)
            title = re.sub(r'\:wiki\:', ' ', title)
            #remove some additional symbols
            desc = re.sub(r'[\=\(\)*.:-]', '', desc)
            title = re.sub(r'[\=\(\)*.:-]', '', title)
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
print(final_result)
#print(title)
#print(desc)
#print(final_tags_string)

#Folder and File locations
#single_files = image_captions_path + image_captions_single_file
#appended_file = image_captions_path + image_captions_appended_file
#Create new file and overwrite if exists

#with open(single_files, 'w') as f:
#    f.write(final_result)
#    f.close
    
#with open(appended_file, 'a') as fa:
#    fa.write(final_result)
#    fa.close

# Closing file
json_read.close()
             


             
             
