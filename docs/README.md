# Caption Scripts

## Caption creation tools

These scripts/tools have been made to assist in the creation of captions for programs such as stable diffusion, utilising existing metadata (from gallery-dl downloads) or editing text files in bulk.

### Now available in tools folder

### json2txt.py

This script can assist in gathering captions from websites that provide useful information such as titles, descriptions, alt descriptions, EXIF data, and tags for media collected using gallery-dl, to generate metadata files (e.g., gallery-dl --write-metadata). The script takes input from a useful, yet randomly organized JSON file and creates a text file with the same name, as well as an appended file.

The contents of the file will be: *Title, Description, Alt_Description, EXIF data, Tags*

As an example: *The Fat Cat Barnaby, Barnaby is always very sleepy and looks drunk, ISO: 200, Focal Length: 100.0, Model is NIKON D850, Aperture: 4.5, Fat Cat, Lazy, sleeping*

The text file will only include elements present in the JSON file, if the JSON is missing any of the following information: title, description, Alt_Description, EXIF, or tags, they will not be included in the text file.

Command line options available with "json2txt.py --help"

### caption2remove.py

This script can aid in replacing specific words within your captions recursively if they are stored in plain text files.

Usage example: captions2remove.py --captiondir c:\captions --caption-find "Monkey Magic is great! --caption-replace "Tripitaka is the best!"

".txt" files are the default file extension but this can be set to any file extension with the extension argument. e.g. captions2remove.py --extension ".json"

Additionally, this script allows you to add text before and after your captions recursively, it does not impose any specific structure so you will need to include delimiters such as "text " or ", text" when doing so.

Command line options available with "captions2remove.py --help"

### plant2caption.py

While this script may not be as useful for general images, it can be beneficial in identifying plants in close-up shots. The script utilizes the Plant Net API, for which a developer account and API key are required. A free account option is available, with a limit of up to 500 API calls per day.

Command line options available with "plant2caption.py --help"

### txts2txt.py

This script simply concatenates all text files (.txt) into one file. It can be useful for creating a file containing all the words used.

This can help create word clouds as well as creating a summary of words used (--dedup)

Command line options available with "txts2txt.py --help"

### txt2wordcloud.py

This script can assist in creating word clouds using tokens or text files utilized in creating captions for images. Additional examples and batch and shell scripts can be found in the examples folder.

Command line options available with "txt2wordcloud.py --help"
