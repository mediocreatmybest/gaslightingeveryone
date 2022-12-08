
import glob
import pathlib
import os
from configparser import ConfigParser
from pathlib import Path





curr_file = pathlib.Path(__file__)
#print(curr_file)


#print('script dir',script_dir)


# http://pymotw.com/2/ConfigParser/
# https://linuxhint.com/python-configparser-example/
# https://zetcode.com/python/configparser/
# https://csatlas.com/python-script-path/

config_parser = ConfigParser()

# Get working directory
#workingdir = pathlib.Path.cwd()
workingdir = Path( __file__ ).parent.absolute()
print('This is the script dir:', workingdir)
configfile = 'conf.ini'
workingconfig = pathlib.Path.joinpath(workingdir, configfile)
read_files = config_parser.read(workingconfig)

print('location of config:', workingconfig)
config_parser.read(workingconfig)
print(config_parser.get('web_config_reddit', 'filter'))
print(config_parser.get('global', 'mode'))




