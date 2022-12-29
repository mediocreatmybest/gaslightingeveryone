# Gaslightingeveryone

This repository contains strong traces gaslighting, along with a few files for; machine learning, containers, and ultimatly some poorly written scripts.

## Caption creation tools

### json2txt.py

This script may help with collecting captions from known websites that give useful; titles, descrptions, exif, tags, for the media.
The script currently takes information from a useful but randomly organised json file and creates a text file next to it based on the same name as well as an appended file.

The contents of the file will be: *Title, Description, EXIF data, Tags*

For example: *The Fat Cat Barnaby, Barnaby is always very sleepy and looks drunk, ISO: 200, Focal Length: 100.0, Model is NIKON D850, Aperture: 4.5, Fat Cat, Lazy, sleeping*

If the json doesn't contain a title, description, EXIF, or tags, it won't get included in the file.

Commandline options available with "python json2txt.py --help"
Config file also available to set image directory.

*TODO:*
Test additional websites.

### caption2remove.py

This script may help with doing a replacement of specific words within your captions recursivly when stored in text type files.

Usage example: python captions2remove.py --captiondir c:\captions --caption-remove "Monkey Magic is great! --caption-replace "Tripitaka is the best!"

".txt" files are the default file extension but this can be set to any file extension with the extension argument. e.g. python captions2remove.py --extension ".json"
