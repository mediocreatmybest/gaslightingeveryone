#Python test script to try clean up some json to txt file captions

import json
import os
import re

# Opening JSON file
jsonfile = open(r"c:\test\file1.jpg.json", "r")
 
  
# returns JSON object as 
# a dictionary
data = json.load(jsonfile)
  
# Iterating through the json
# list
#for i in data['tags']:
#    print(i)

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

#Create new file and overwrite if exists

with open('caption.txt', 'w') as f:
    f.write(final_result)
    f.close

# Closing file
jsonfile.close()
