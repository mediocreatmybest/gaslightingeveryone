import subprocess
#import csv
import sys
import urllib
import urllib.request
from configparser import ConfigParser
import argparse
import pathlib
from pathlib import Path
from tqdm import tqdm
from time import sleep

# This script is intended to be used with plain text only

# List of supported sites.
SUPPORTED_FILTER_URLS = ['www.reddit.com', 'www.unsplash.com', 'www.artstation.com']

# Define our functions

# Function to check if the data is a valid url
def urldatacheck(urldata):
        """ Simple function to check if this is a valid URL, returns: True or False """

        function_url = urllib.parse.urlparse(urldata)

        if function_url.netloc == '':
            return False
        else:
            return True

def starttaskprog(task):
    """ Subprocess task function, should start a subprocess """
    #subprocess.Popen(args, bufsize=0, executable=None, stdin=None, stdout=None,
    #stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None,
    #env=None, universal_newlines=False, startupinfo=None, creationflags=0)
    #https://gist.github.com/timothymugayi/fee21fd931d3b03ed62a32c14534bc96
    try:
        with tqdm(unit='B', unit_scale=True, miniters=1, desc="run_task={}".format(task)) as t:
            process = subprocess.Popen(task, shell=True, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # print subprocess output line-by-line as soon as its stdout buffer is flushed in Python 3:
            for line in process.stdout:
                # Update the progress, since we do not have a predefined iterator
                # tqdm doesnt know before hand when to end and cant generate a progress bar
                # hence elapsed time will be shown, this is good enough as we know
                # something is in progress
                t.update()
                # forces stdout to "flush" the buffer
                sys.stdout.flush()

            process.stdout.close()

            return_code = process.wait()

            if return_code != 0:
                raise subprocess.CalledProcessError(return_code, task)

    except subprocess.CalledProcessError as e:
        sys.stderr.write(
            "common::run_command() : [ERROR]: output = %s, error code = %s\n"
            % (e.output, e.returncode))

def starttask(task):
    """ Subprocess task function, should start a subprocess """
    process = subprocess.Popen(task,
                               shell=True,
                               bufsize=1,
                               universal_newlines=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return_code = process.wait()
    if return_code != 0:
        print(f'Error# Code: {return_code}')
        #raise subprocess.CalledProcessError(return_code, task)
    if return_code == 0:
        print(f'Error# Code: {return_code}')
        print('Yay')

# Create ConfigParser
config_parser = ConfigParser()

# Get the scripts parent directory so we can locate the config file
workingdir = Path(__file__).parent

# Name of working config file
# *Todo: * Switch this to a list, just because
configfile = 'config.ini'

# Join the working parent directory with the config file
workingconfig = pathlib.Path.joinpath(workingdir, configfile)

# read config file
read_files = config_parser.read(workingconfig)

# Create the parser
parser = argparse.ArgumentParser()
# Command line arguments will overrule the config file (ideally)
parser.add_argument('--downloader', type=str, choices=['gallery-dl', 'yt-dlp'], required=False)
parser.add_argument('--arg', type=str, required=False)
parser.add_argument('--type', type=str, choices=['url', 'file'], required=False)
parser.add_argument('--mode', type=str, choices=['csv', 'txt'], required=False)
parser.add_argument('--sourcelist', type=str, required=False)
parser.add_argument('--directory', type=str, required=False)

# Parse the arguments
CMD_ARGS = parser.parse_args()

# Gallery-DL defaults
GALLERY_CMD = 'gallery-dl'
GALLERY_ARG = '--write-metadata --sleep 2-4 --range 1-1'

# YT-DLP Defaults ######## To do ######
YTDLP_CMD = 'yt-dlp'
YTDLP_ARG = '--write-info-json'

# Set Defaults if non selected
if CMD_ARGS.downloader is None:
    downloader = config_parser.get('downloaders', 'program')
else:
    downloader = CMD_ARGS.downloader

if CMD_ARGS.arg is None:
    downloaderarg = config_parser.get('downloaders', 'arguments')
else:
    downloaderarg = CMD_ARGS.arg

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
    EXTRACTPATH = f'--directory {DIRLOC}'
else:
    EXTRACTPATH = f'--directory {CMD_ARGS.directory}'


#print('program selected is:', downloader)
#print('source list type is:', SRC_LIST_TYPE)
#print('The global mode is:', GLOBAL_MODE)
#print('program source list is:', TXT_SRC)

# URL filters for supported websites (reddit, etc.)
# This will allow us to loop through each type of top search
REDDIT_TOP = config_parser.get('web_config_reddit', 'filter')
UNSPLASH_SEARCH_FILTER = config_parser.get('web_config_unsplash', 'filter')
ARTSTATION_SEARCH_FILTER = config_parser.get('web_config_unsplash', 'filter')

# Build the command and argument list
taskseq = []
taskseq = downloader.split() + EXTRACTPATH.split() + downloaderarg.split()

# Parse URL details from https://www.simplified.guide/python/get-host-name-from-url
# https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse

#print('global mode is now:', GLOBAL_MODE)
#print('SRC_LIST is now:', SRC_LIST_TYPE)

#sys.exit()

# Using plain text data as input data
if GLOBAL_MODE == 'txt' and SRC_LIST_TYPE == 'url':
    # Check if we are using a websites data
    if urldatacheck(TXT_SRC) is True:
        TXT_URL = TXT_SRC
        with urllib.request.urlopen(TXT_URL) as TXT_READ:
            # Read, decode and then split the final data
            # from the webserver to allow reading each line
            rawoutput = TXT_READ.read().decode('UTF-8').split()
            # Loop through each line with tqdm as the progress bar
            pbar = tqdm(rawoutput, unit='scraps')
            #for eachdomain in tqdm(rawoutput, unit="downloads"):
            for rawoutput in pbar:
                urlcheck = urllib.parse.urlparse(rawoutput).netloc
                pbar.set_description(f'{urlcheck}')
                #pbar.set_description('URL')
                # Do a check against each domain as they may have different options
                # Create URL Check Variable, not sure if this will work...
                #urlcheck = urllib.parse.urlparse(eachdomain).netloc
                urlcheck = urllib.parse.urlparse(rawoutput).netloc
                #sleep(0.5)

                if urlcheck == 'www.reddit.com':
                        #print('Reddit! Beep Boop!')
                        taskseq.append(rawoutput)
                        starttask(taskseq)
                        taskseq = taskseq[ : -1]

                if urlcheck == 'www.unsplash.com':
                    #print('Unsplash! Beep! Boop!')
                    taskseq.append(rawoutput)
                    starttask(taskseq)
                    taskseq = taskseq[ : -1]

                if urlcheck == 'www.artstation.com':
                    #print('Artstation! Beep Boop!'
                    taskseq.append(rawoutput)
                    starttask(taskseq)
                    taskseq = taskseq[ : -1]

                # Catch any websites that don't exist in the supported filter and do standard download
                if urlcheck != SUPPORTED_FILTER_URLS:
                    #print('CATCHALL! Beep Boop!')
                    taskseq.append(rawoutput)
                    starttask(taskseq)
                    taskseq = taskseq[ : -1]






    ##Check if we are using a text file for data #Also this is broken.
    if urldatacheck(TXT_SRC) is False:
        TXT_FILE = Path(rf'{TXT_SRC}')
        print('TXT MODE!')
        print('The test path is:')
        print(TXT_FILE)


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

