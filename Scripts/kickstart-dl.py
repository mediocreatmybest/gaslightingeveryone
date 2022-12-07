import subprocess
import csv
import urllib
import urllib.request
import argparse
from pathlib import Path

# This script is intended to be used with plain text only

# List of supported sites.
SUPPORTED_FILTER_URLS = ['www.reddit.com','www.unsplash.com', 'www.artstation.com']
# URL filters for supported websites (reddit, etc.) This will allow us to loop through each type of top search
REDDIT_TOP = ['/top/?t=all','/top/?t=month']
UNSPLASH_SEARCH_FILTER = ['/cats?orientation=squarish']
ARTSTATION_SEARCH_FILTER = ['?sort_by=rank']

# Gallery-DL defaults
GALLER_CMD ='gallery-dl'
GALLERY_ARG = '--write-metadata --sleep 2-4 --range 1-1'


# YT-DLP Defaults ######## To do ######
YTDLP_CMD = 'yt-dlp'
YTDLP_ARG = '--write-info-json'


# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--downloader', type=str, choices=['gallery-dl', 'yt-dlp'], required=False)
parser.add_argument('--type', type=str, choices=['url', 'file'], required=False)
parser.add_argument('--txtmode', type=str, choices=['csv', 'plain'], required=False)
parser.add_argument('--sourcelist', type=str, required=True)
parser.add_argument('--directory', type=str, required=True)


# Parse the argument
CMD_ARGS = parser.parse_args()

# Set Defaults if non selected
if CMD_ARGS.downloader == None:
    CMD_ARGS.downloader = 'gallery-dl'
if CMD_ARGS.type == None:
    CMD_ARGS.type = 'url'
if CMD_ARGS.txtmode == None:
    CMD_ARGS.txtmode = 'plain'

print('program selected is:', CMD_ARGS.downloader)
print('program type is:', CMD_ARGS.type)
print('program mode is:', CMD_ARGS.txtmode)
print('program source list is:', CMD_ARGS.sourcelist)


# Set this based on command line arguments or defaults
if CMD_ARGS.txtmode == 'plain':
    CSV_MODE = False
else:
    CSV_MODE = True

#Set this based on command line arguments or defaults
if CMD_ARGS.type == 'url':
    FILE_MODE = False
else:
    FILE_MODE = True

#Set this based on command line arguments
#Currently file source is broken, only a url with raw text will work
TXT_SRC = CMD_ARGS.sourcelist

#Set directory location based off command line arguments
GALLERY_EXTRACT_PATH = f'--directory {CMD_ARGS.directory}'
YTDLP_DL_PATH = f'--output {CMD_ARGS.directory}'

#Organise defaults into single string
GALLERY_FULLCMDARG = GALLER_CMD.split() + GALLERY_EXTRACT_PATH.split() + GALLERY_ARG.split()

#Doesn't really need to be a function but might as well see if this works.
#Function to check if the data is parsed as a url, might not be the best way to do it.
def is_url_data_type():
    #print('Checking if text source is URL')
    function_url = urllib.parse.urlparse(TXT_SRC)
    if function_url != '':
        return True

#Parse URL details from https://www.simplified.guide/python/get-host-name-from-url
#https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse

#Using plain text data as input data
if CSV_MODE == False:
    #Check if we are using a websites data
    if is_url_data_type() is True:
        txt_url = TXT_SRC
        with urllib.request.urlopen(txt_url) as txt_read:
            #Read, decode and then split the final data from the webserver to allow reading each line
            rawoutput = txt_read.read().decode('utf-8').split()
            #Loop through each line
            for eachdomain in rawoutput:

                #Do a check against each domain as they may have different options
                #Create URL Check Variable, not sure if this will work...
                urlcheck = urllib.parse.urlparse(eachdomain).netloc
                if urlcheck == 'www.reddit.com':
                    for topsearch in REDDIT_TOP:
                        EACHDOMAIN_TOP = eachdomain + topsearch
                        GALLERY_FULLCMDARG.append(EACHDOMAIN_TOP)
                        result = subprocess.run(GALLERY_FULLCMDARG, capture_output=True, text=True, encoding='UTF-8')

                if urlcheck == 'www.unsplash.com':
                    GALLERY_FULLCMDARG.append(eachdomain)
                    result = subprocess.run(GALLERY_FULLCMDARG, capture_output=True, text=True)

                if urlcheck == 'www.artstation.com':
                    GALLERY_FULLCMDARG.append(eachdomain)
                    result = subprocess.run(GALLERY_FULLCMDARG, capture_output=True, text=True)

                #if (web1 != query and web2 != query and web3 != query):
                #   print('This should only be triggered if Web1 and Web2 and Web3 are not found')

                #Catch any websites that don't exist in the supported filter and do standard download
                if (urlcheck != SUPPORTED_FILTER_URLS):
                    GALLERY_FULLCMDARG.append(eachdomain)
                    result = subprocess.run(GALLERY_FULLCMDARG, capture_output=True, text=True)






    #Check if we are using a text file for data #Also this is broken.
    if is_url_data_type() is False:
        txt_file = Path(rf'{TXT_SRC}')  #Broken
        print ('TXT MODE!')
        print ('The test path is')
        print(txt_file)


#Using CSV seperated data instead of plain text.
if CSV_MODE == True:
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