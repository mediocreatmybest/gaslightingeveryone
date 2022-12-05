import subprocess
import csv
import urllib
import urllib.request
import argparse
from pathlib import Path

#This script is intended to be used with plain text only

#List of supported sites.
supported_filter_urls = ['www.reddit.com','www.unsplash.com']
#URL filters for supported websites (reddit, etc.) This will allow us to loop through each type of top search
reddit_top = ['/top/?t=all','/top/?t=month']
unsplash_search_filter = ['/cats?orientation=squarish']
artstation_search_filter = ['?sort_by=rank']

#Gallery-DL defaults
gallery_cmd ='gallery-dl'
gallery_arg = '--write-metadata --sleep 2-4 --range 1-1'


#YT-DLP Defaults ######## To do ######
ytdlp_cmd = 'yt-dlp'
ytdlp_arg = '--write-info-json'


# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--downloader', type=str, choices=['gallery-dl', 'yt-dlp'], required=False)
parser.add_argument('--type', type=str, choices=['url', 'file'], required=False)
parser.add_argument('--txtmode', type=str, choices=['csv', 'plain'], required=False)
parser.add_argument('--sourcelist', type=str, required=True)
parser.add_argument('--directory', type=str, required=True)


# Parse the argument
cmd_args = parser.parse_args()

#Set Defaults if non selected
if cmd_args.downloader == None: 
    cmd_args.downloader = 'gallery-dl'
if cmd_args.type == None: 
    cmd_args.type = 'url'
if cmd_args.txtmode == None: 
    cmd_args.txtmode = 'plain'
  
print('program selected is:', cmd_args.downloader)
print('program type is:', cmd_args.type)
print('program mode is:', cmd_args.txtmode)
print('program source list is:', cmd_args.sourcelist)


#Set this based on command line arguments or defaults
if cmd_args.txtmode == 'plain': 
    csv_mode = False
else:
    csv_mode = True

#Set this based on command line arguments or defaults
if cmd_args.type == 'url':
    file_mode = False
else:
    file_mode = True

#Set this based on command line arguments
#Currently file source is broken, only a url with raw text will work
txt_src = cmd_args.sourcelist

#Set directory location based off command line arguments
gallery_extract_path = f'--directory {cmd_args.directory}'
ytdlp_dl_path = f'--output {cmd_args.directory}'

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
                #Create URL Check Variable, not sure if this will work...
                urlcheck = urllib.parse.urlparse(eachdomain).netloc    
                if urlcheck == 'www.reddit.com':
                    for topsearch in reddit_top:
                        eachdomain_top = eachdomain + topsearch
                        gallery_full_cmdarg.append(eachdomain_top)
                        result = subprocess.run(gallery_full_cmdarg, capture_output=True, text=True, encoding='UTF-8')
                                        
                if urlcheck == 'www.unsplash.com':
                    gallery_full_cmdarg.append(eachdomain)
                    result = subprocess.run(gallery_full_cmdarg, capture_output=True, text=True)
                                        
                if urlcheck == 'www.artstation.com':
                    gallery_full_cmdarg.append(eachdomain)
                    result = subprocess.run(gallery_full_cmdarg, capture_output=True, text=True)
                    
                #if (web1 != query and web2 != query and web3 != query):
                #   print('This should only be triggered if Web1 and Web2 and Web3 are not found')
                
                #Catch any websites that don't exist in the supported filter and do standard download
                if (urlcheck != supported_filter_urls):
                    gallery_full_cmdarg.append(eachdomain)
                    result = subprocess.run(gallery_full_cmdarg, capture_output=True, text=True)
                     
                
                
                                        

                        
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

#if result.stdout:
#    print('\n')
#    print('###############################')
#    print('Progress was made! Check logs.')
#    print('###############################')
#    print('\n')
    
#if result.stderr:
#    print('\n')
#    print('###############################')
#    print('Errors found, please check logs')
#    print('###############################')
#    print('\n') 
#
print('###############################')
print('errors:')
print (result.stderr)
print('###############################')
print('Results:')
print (result.stdout)
print('###############################')