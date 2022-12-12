# Gaslightingeveryone
This repository contains strong traces gaslighting, along with a few files for; machine learning, containers, and ultimatly some poorly written scripts.

## Caption creation tools
### json2txt.py:
This script may help with collecting captions from known websites that give useful; titles, descrptions, exif, tags, for the media.
The script currently takes information from a useful but randomly organised json file and creates a text file next to it based on the same name as well as an appended file.

The contents of the file will be: *Title, Description, EXIF data, Tags*

For example: *The Fat Cat Barnaby, Barnaby is always very sleepy and looks drunk, ISO: 200, Focal Length: 100.0, Model is NIKON D850, Aperture: 4.5, Fat Cat, Lazy, sleeping*

If the json doesn't contain a title, description, EXIF, or tags, it won't get included in the file.

Commandline options available with "python json2txt.py --help"
Config file also available to set image directory.

*TODO:*
Test additional websites.

### kickstart-dl.py:
This script is partially broken and unfinished, it should help kick start the download process for gallery-dl, ultimatly it is just a wrapper script to hopefully house a few downloaders along with some filters for some websites into a single clunky script.

*TODO:*
Add additional download, fix std.err output, create log files.





