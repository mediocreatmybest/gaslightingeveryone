import subprocess
import re
import csv
import urllib
import urllib.request
from pathlib import Path

#This script is intended to be used with plain text only
#Text should be a list of URLs for gallery-dl to download

#Set to True if source list data is in csv format such as https://example.com/image.png, Description
#To Do 
csv_mode = False
#Set to False if you are reading a URL or True if you are reading a txt file
#file_mode = True
#configure download path 

#Set txt source, can be plain text file or URL
txt_src = 'http://x.x.x.x/example.txt'
#txt_src = 'c:\images'

#List of supported sites. #to do.
supported_sites = []
#URL filters for supported websites (reddit, etc.) This will allow us to loop through each prefered top search
#To Do: Check other websites
reddit_top = ['/top/?t=all','/top/?t=month']
unsplash_search_filter = ['/cats?orientation=squarish']
artstation_search_filter = ['?sort_by=rank']

#Gallery-DL defaults
gallery_cmd ='gallery-dl'
gallery_arg = '--write-metadata --download-archive archivedata.txt --sleep 2-4'
gallery_extract_path = '--directory c:\images'

#Organise defaults into single string
gallery_full_cmdarg = gallery_cmd.split() + gallery_extract_path.split() + gallery_arg.split()

#Doesn't really need to be a function but might as well see if this works. 
#Function to check if the data is parsed as a url, might not be the best way to do it. 
def is_url_data_type():
    #print('Checking if text source is URL')
    function_url = urllib.parse.urlparse(txt_src)
    if function_url != '':
        return True
    else:
        return False

#Parse URL details from https://www.simplified.guide/python/get-host-name-from-url
#https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse

#Using plain text data as input data
if csv_mode == False:
    #Check if we are using a websites data
    if is_url_data_type() is True:
        txt_url = txt_src     
        with urllib.request.urlopen(txt_url) as txt_read:
            #Read, decode and then split the final data from the webserver to allow reading each line
            rawoutput = txt_read.read().decode('utf-8').split()
            #Loop through each line
            for eachdomain in rawoutput:
                
                #Do a check against each domain as they may have different options            
                if urllib.parse.urlparse(eachdomain).netloc == 'example.com':
                    for topsearch in reddit_top:
                        eachdomain_top = eachdomain + topsearch
                        #print(eachdomain_top)
                        gallery_full_cmdarg.append(eachdomain_top)
                        result = subprocess.run(gallery_full_cmdarg, capture_output=True, text=True)
                                        
                if urllib.parse.urlparse(eachdomain).netloc == 'www.test.example.com':
                    gallery_full_cmdarg.append(eachdomain)
                    result = subprocess.run(gallery_full_cmdarg, capture_output=True, text=True)
                                        
                if urllib.parse.urlparse(eachdomain).netloc == 'www.domain.example.com':
                    gallery_full_cmdarg.append(eachdomain)
                    result = subprocess.run(gallery_full_cmdarg, capture_output=True, text=True)
                    
                if (urllib.parse.urlparse(eachdomain).netloc != 'www.domain.example.com'):
                    test = test 
                    #for urllib.parse.urlparse(eachdomain).netloc in supported_sites: print(supported_sites) 
                     
                
                
                                        
#if (web1 != query and web2 != query and web3 != query):
 #   print('This should only be triggered if Web1 and Web2 and Web3 are not found')
                        
    #Check if we are using a text file for data #Also this is broken.
    if is_url_data_type() is False:
        txt_file = Path(rf'{txt_src}')  #Broken
        print ('TXT MODE!')
        print ('The test path is')
        print(txt_file)
        
   
#Using CSV seperated data instead of plain text. 
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





#Give single message, or two.

if result.stdout:
    print('\n')
    print('###############################')
    print('Progress was made! Check logs.')
    print('###############################')
    print('\n')
    
if result.stderr:
    print('\n')
    print('###############################')
    print('Errors found, please check logs')
    print('###############################')
    print('\n') 

#print('###############################')
#print("\n")
#print (result.stderr)
#print("\n")
#print('###############################')
#print("\n")
#print (result.stdout)
#print("\n")
#print('###############################')
