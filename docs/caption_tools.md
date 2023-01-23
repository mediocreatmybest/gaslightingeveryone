# Caption Scripts

## Caption creation tools

These scripts have been created to help with creating captions for programs such as stable diffusion with existing metadata (from gallery-dl downloads) or to help edit the text files in bulk.

### Now available in tools folder

### json2txt.py

This script may help with collecting captions from known websites that give useful; titles, descrptions, alt descriptions, exif, tags, for the media collected using gallery-dl to create metadata files (e.g. gallery-dl --write-metadata).
The script currently takes information from a useful but randomly organised json file and creates a text file next to it based on the same name as well as an appended file.

The contents of the file will be: *Title, Description, Alt_Description, EXIF data, Tags*

For example: *The Fat Cat Barnaby, Barnaby is always very sleepy and looks drunk, ISO: 200, Focal Length: 100.0, Model is NIKON D850, Aperture: 4.5, Fat Cat, Lazy, sleeping*

If the json doesn't contain a title, description, Alt_Description, EXIF, or tags, it won't get included in the file.

Commandline options available with "python json2txt.py --help"
Config file also available to set image directory. (To be removed)

### caption2remove.py

This script may help with doing a replacement of specific words within your captions recursivly when stored in text type files.

Usage example: python captions2remove.py --captiondir c:\captions --caption-find "Monkey Magic is great! --caption-replace "Tripitaka is the best!"

".txt" files are the default file extension but this can be set to any file extension with the extension argument. e.g. python captions2remove.py --extension ".json"

You can also prepend and append text to captions recursivly. The script doesn't assume structure, so you need to include seperators e.g. "text " or ", text".

### plant2caption.py

This script is less useful for general images but can be useful in identifying plants that you may have close ups.
The script uses Plant NET API and you will need to sign up to a developer account with an API key. They have a free accounts that allows up to 500 API calls a day.
Commandline options available with "python plant2caption.py --help"

### txts2txt.py

This is a simple script that will concatenate all text files (.txt) into a single file.
This can be useful when you want to have a file of all available words used.

This can help create wordclouds as well as creating a summary of words use (--dedup)
Commandline options available with "python txts2txt --help"

### txt2wordcloud.py

This script may be useful to get an idea of creating word clouds with  tokens or text files you have used in creating captions for images.
Other examples are available in the examples folder with batch (.bat) and shell (.sh) scripts.
