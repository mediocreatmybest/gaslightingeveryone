import subprocess
import csv
import urllib
import urllib.request
from configparser import ConfigParser
import argparse
import pathlib
from pathlib import Path

# This script is intended to be used with plain text only

# List of supported sites.
SUPPORTED_FILTER_URLS = ['www.reddit.com','www.unsplash.com', 'www.artstation.com']

# Gallery-DL defaults
GALLER_CMD ='gallery-dl'
GALLERY_ARG = '--write-metadata --sleep 2-4 --range 1-1'

# YT-DLP Defaults ######## To do ######
YTDLP_CMD = 'yt-dlp'
YTDLP_ARG = '--write-info-json'

config_parser = ConfigParser()

# Get the scripts parent directory so we can locate the config file

workingdir = Path( __file__ ).parent.absolute()
# print('This is the script dir:', workingdir)

# Name of working config file
# *Todo: * Switch this to a list, just because
configfile = 'config.ini'

# Join the working parent directory with the config file
workingconfig = pathlib.Path.joinpath(workingdir, configfile)

# Set how to read the contents of the config
read_files = config_parser.read(workingconfig)

# Create the parser
parser = argparse.ArgumentParser()
# Command line arguments will overrule the config file (ideally)
parser.add_argument('--downloader', type=str, choices=['gallery-dl', 'yt-dlp'], required=False)
parser.add_argument('--type', type=str, choices=['url', 'file'], required=False)
parser.add_argument('--mode', type=str, choices=['csv', 'txt'], required=False)
parser.add_argument('--sourcelist', type=str, required=False)
parser.add_argument('--directory', type=str, required=False)


# Parse the argument
CMD_ARGS = parser.parse_args()

# Set Defaults if non selected
if CMD_ARGS.downloader is None:
    CMD_ARGS.downloader = 'gallery-dl'
if CMD_ARGS.type is None:
    SRC_LIST_TYPE = config_parser.get('src_list', 'type')
else:
    SRC_LIST_TYPE = CMD_ARGS.type

if CMD_ARGS.mode is None:
    GLOBAL_MODE = config_parser.get('global', 'mode')
else:
    GLOBAL_MODE = CMD_ARGS.mode
if CMD_ARGS.sourcelist is None:
    TXT_SRC = config_parser.get('src_list', 'txt_src')
else:
    TXT_SRC = CMD_ARGS.sourcelist

# Set directory location based off command line arguments or config file
if CMD_ARGS.directory is None:
    DIRLOC = config_parser.get('global', 'directory')
    GALLERY_EXTRACT_PATH = f'--directory {DIRLOC}'
    YTDLP_DL_PATH = f'--output {DIRLOC}'
else:
    GALLERY_EXTRACT_PATH = f'--directory {CMD_ARGS.directory}'
    YTDLP_DL_PATH = f'--output {CMD_ARGS.directory}'

print('program selected is:', CMD_ARGS.downloader)
print('source list type is:', SRC_LIST_TYPE)
print('The global mode is:', GLOBAL_MODE)
print('program source list is:', TXT_SRC)

# URL filters for supported websites (reddit, etc.) This will allow us to loop through each type of top search
REDDIT_TOP = config_parser.get('web_config_reddit', 'filter')
UNSPLASH_SEARCH_FILTER = config_parser.get('web_config_unsplash', 'filter')
ARTSTATION_SEARCH_FILTER = config_parser.get('web_config_unsplash', 'filter')

# Organise defaults into single string
GALLERY_FULLCMDARG = GALLER_CMD.split() + GALLERY_EXTRACT_PATH.split() + GALLERY_ARG.split()

# Doesn't really need to be a function but might as well see if this works.
# Function to check if the data is parsed as a url, might not be the best way to do it.

def is_url_data_type():
        print('Checking if text source is URL')
        function_url = urllib.parse.urlparse(TXT_SRC)
        # print(function_url.path)
        # print(function_url)
        if function_url.netloc == '':
            print('netloc is empty')
            print('path is:', function_url.path)
            print('this does not pass the url sniff test')
            return False
        else:
            print('netloc has data')
            print('netloc is:', function_url.netloc)
            return True


# Parse URL details from https://www.simplified.guide/python/get-host-name-from-url
# https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse

print('global is now:',  GLOBAL_MODE)
print('SRC_LIST is now:',  SRC_LIST_TYPE)


# Using plain text data as input data
if GLOBAL_MODE == 'txt' and SRC_LIST_TYPE == 'url':
    print('GLOBAL MODE IS TXT AND SRC LIST TYPE IS URL')
    # Check if we are using a websites data
    if is_url_data_type() is True:
        TXT_URL = TXT_SRC
        print(TXT_URL)
        with urllib.request.urlopen(TXT_URL) as TXT_READ:
            # Read, decode and then split the final data from the webserver to allow reading each line
            rawoutput = TXT_READ.read().decode('UTF-8').split()
            # Loop through each line
            for eachdomain in rawoutput:

                # Do a check against each domain as they may have different options
                # Create URL Check Variable, not sure if this will work...
                urlcheck = urllib.parse.urlparse(eachdomain).netloc
                if urlcheck == 'www.reddit.com':
                    for topsearch in REDDIT_TOP:
                        EACHDOMAIN_TOP = eachdomain + topsearch
                        GALLERY_FULLCMDARG.append(EACHDOMAIN_TOP)
                        print('Reddit! Beep Boop!')
                        #result = subprocess.run(GALLERY_FULLCMDARG, capture_output=True, text=True, encoding='UTF-8')

                if urlcheck == 'www.unsplash.com':
                    GALLERY_FULLCMDARG.append(eachdomain)
                    print('Unsplash! Beep! Boop!')
                    #result = subprocess.run(GALLERY_FULLCMDARG, capture_output=True, text=True)

                if urlcheck == 'www.artstation.com':
                    GALLERY_FULLCMDARG.append(eachdomain)
                    print('Artstation! Beep Boop!')
                    #result = subprocess.run(GALLERY_FULLCMDARG, capture_output=True, text=True)

                # Catch any websites that don't exist in the supported filter and do standard download
                if (urlcheck != SUPPORTED_FILTER_URLS):
                    GALLERY_FULLCMDARG.append(eachdomain)
                    print('CATCHALL! Beep Boop!')
                    #result = subprocess.run(GALLERY_FULLCMDARG, capture_output=True, text=True)






    ##Check if we are using a text file for data #Also this is broken.
    #if is_url_data_type() is False:
    #    TXT_FILE = Path(rf'{TXT_SRC}')  #Broken
    #    print ('TXT MODE!')
    #    print ('The test path is')
    #    print(TXT_FILE)


#Using CSV seperated data instead of plain text.
#if GLOBAL_MODE == 'csv':
#    with open(TXT_FILE) as csv_file:
#        csv_reader = csv.reader(csv_file, delimiter=',')
#        for row in csv_reader:
#            download = (row[0])
#            #domain_details = (row[1])
#            url = urllib.parse.urlparse(row[0])
#            print(url.netloc)
#            #print(is_valid_hostname(download))
#            print('CSV MODE!')





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
#print('###############################')
#print('errors:')
#print (result.stderr)
#print('###############################')
#print('Results:')
#print (result.stdout)
#print('###############################')