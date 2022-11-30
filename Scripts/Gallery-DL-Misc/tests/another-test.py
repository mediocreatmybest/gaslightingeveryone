import os
import subprocess
import re
import csv
import urllib
import urllib.request
#import validators #install validators
from pathlib import Path


#Set to True if data is csv such as https://example.com/image.png, Description
#To Do 
csv_mode = False
#Set to False if you are reading a URL or True if you are reading a txt file
file_mode = True
#configure download path 
image_captions_path = Path(r"c:\images")
#Set txt source, can be plain text file or URL
txt_src = 'http://10.254.14.136/example.txt'
#txt_src = 'c:\images'
#URL filters for supported websites (reddit, etc.)
reddit_top = ['/top/?t=all','/top/?t=month']


#with urllib.request.urlopen(txt_url) as open_txt_url:
#    data_txt_url = open_txt_url.read()
#    print(data_txt_url)

# Check if this is a hostname not
def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

#print(is_valid_hostname('google.com'))

#Doesn't really need to be a function but might as well see if this works. 
def is_url_data_type():
    #print('Checking if text source is URL')
    function_url = urllib.parse.urlparse(txt_src)
    if function_url != '':
        return True
    else:
        return False

#Functions everywhere!
def superfunction():
    #do something
    print('Super duper function')
    

#Parse URL details from https://www.simplified.guide/python/get-host-name-from-url
#https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse



if csv_mode == False:
    if is_url_data_type() is True:
        txt_url = txt_src     
        with urllib.request.urlopen(txt_url) as txt_read:
            #print('URL MODE!')
            rawoutput = txt_read.read().decode('utf-8').split()
            #Loop through each line
            for eachdomain in rawoutput:
                #Do a check against each domain as they may have different options            
                if urllib.parse.urlparse(eachdomain).netloc == 'example.com':
                    #Do something here
                    print(f'Run command \'xyz\' --test {eachdomain}/top/?t=all')
                    print(f'Run command \'test\' --test {eachdomain}/top/?t=month')
                                                 
                if urllib.parse.urlparse(eachdomain).netloc == 'www.test.example.com':
                    #Do something else
                    print(f'Run command \'xyz\' --test {eachdomain}/top/?t=all')
                    print(f'Run command \'test\' --test {eachdomain}/top/?t=month')
                    
                if urllib.parse.urlparse(eachdomain).netloc == 'www.domain.example.com':
                    #Do something else
                    print(f'Run command \'xyz\' --test {eachdomain}/top/?t=all')
                    print(f'Run command \'test\' --test {eachdomain}/top/?t=month')
    
    
    if is_url_data_type() is False:
        txt_file = Path(rf'{txt_src}')  #Broken
        print ('TXT MODE!')
        print ('The test path is')
        print(txt_file)
        
        
        


if csv_mode == True:
    with open(txt_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            download = (row[0])
            #domain_details = (row[1])
            url = urllib.parse.urlparse(row[0])
            print(url.netloc)
            #print(is_valid_hostname(download))
            print('CSV MODE!')


    
    
        
        
        






#subprocess.run(['gallery-dl', '--download-archive archivedata.txt', '--write-metadata','--sleep 2-4','--range 1-300','r:https:url.com/raw/text',])
#subprocess.run(['gallery-dl', '--download-archive archivedata.txt', '--write-metadata','--sleep 2-4','r:https:url.com/raw/text',])
#subprocess_args = ['--download-archive archivedata.txt --write-metadata --sleep 2-4 --range 1-300']
#command = ['gallery-dl']
#command.extend(subprocess_args)

subprocess.run(['gallery-dl', '--download-archive archivedata.txt --write-metadata --sleep 2-4 --range 1-300'])