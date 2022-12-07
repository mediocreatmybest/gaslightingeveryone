
from configparser import ConfigParser
import glob
import pathlib

curr_file = pathlib.Path(__file__)
print(curr_file)


config_parser = ConfigParser()
# http://pymotw.com/2/ConfigParser/
# https://linuxhint.com/python-configparser-example/
# https://zetcode.com/python/configparser/


# Get working directory
workingdir = pathlib.Path.cwd()
configfile = 'json2txt.conf'
workingconfig = pathlib.Path(workingdir, configfile)
read_files = config_parser.read(workingconfig)

config_parser.read(workingconfig)

print(config_parser.get('json2txt', 'filters'))





