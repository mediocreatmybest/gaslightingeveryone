# Caption Scripts

## Caption creation tools

These scripts/tools have been made to assist in the creation of captions for programs such as stable diffusion, utilising existing metadata (from gallery-dl downloads) or editing text files in bulk.

### Main tools are located in the tools folder

### json2txt.py

This script can assist in gathering captions from websites that provide useful information such as titles, descriptions, alt descriptions, EXIF data, and tags for media collected using gallery-dl, to generate metadata files (e.g., gallery-dl --write-metadata). The script takes input from a useful, yet randomly organized JSON file and creates a text file with the same name, as well as an appended file.

The contents of the file will be: *Title, Description, Alt_Description, EXIF data, Tags*

As an example: *The Fat Cat Barnaby, Barnaby is always very sleepy and looks drunk, ISO: 200, Focal Length: 100.0, Model is NIKON D850, Aperture: 4.5, Fat Cat, Lazy, sleeping*

The text file will only include elements present in the JSON file, if the JSON is missing any of the following information: title, description, Alt_Description, EXIF, or tags, they will not be included in the text file.

Command line options available with "json2txt.py --help"

### json2caption.py

json2caption.py is a script that can help create captions for your images by collecting all the values from the json metadata that was downloaded or created with the images, including headings, and creating a plain text file (txt, tags, caption). It also includes a word swap feature to replace certain words with others using a basic text file.

#### Usage

To use the script on simple json files, you can use the following command:

json2caption.py "/image/directory or c:\images\images" --filter "tags: " --keys "tags"

This will create a file in the same directory with .tags by default.

For json files with a less than standard structure, you can use additional filter files:

json2caption.py "/image/directory or c:\images\images" --filter-file "filter_file.txt" --word-swap "word_swap_dictionary.txt" --keys "tags"

The filter_file.txt is a Python regex and each new line is a new filter. The word_swap_dictionary is a simple dictionary file with words separated by a colon. Each new line is a new word swap filter.

#### Options

There are quite a few options available for the script, including filters and word swaps. Please use the --help option for more information.

#### Note

This script has been made to fix some issues with the initial json2txt.py script. While it may be elaborate for something that could have been done in a simpler way, it aims to provide a more comprehensive way to help create captions for images from existing data, or not.
See the example folder with filter_files for some of the basic filtering options.

### captions2merge.py

captions2merge.py can be used to merge captions from image files into a single plain text file.

To use the script, specify the input directory containing the image files using the --input-dir option. By default, the script will merge .caption and .tags files together to create image1.txt. You can also select any plain text file to merge.

e.g.

captions2merge.py --input-dir "/images/ or C:\images"

Note:

The script currently does not check for random or misplaced commas. It is recommended to copy a few files to test or check the data first.

### captions2remove.py

This script can aid in replacing specific words within your captions recursively if they are stored in plain text files.
".txt" files are the default file extension but this can be set to any file extension with the extension argument. e.g. captions2remove.py --extension ".json"

Usage example: captions2remove.py --captiondir c:\captions --caption-find "Monkey Magic is great! --caption-replace "Tripitaka is the best!"

Additionally, this script allows you to add text before and after your captions recursively, it does not impose any specific structure so you will need to include delimiters such as "text " or ", text" when doing so.

Command line options available with "captions2remove.py --help"

### images2resize.py

This script now has a few *"attempted"* options:

* Multiples Crop (--multiples-crop): Crops the edges of an image to the closest multiple of a specified number of pixels (e.g. 64 pixels for a 1024x768 image).
* Aspect Ratio Crop (--aspect-crop): Crops the image to the closest specified aspect ratio (1,1.33,1.5,etc.), but wil not enlarge the image.
* Resize on Small Side *(I'm sure this could have a better name)* (--resize-small-side): Shrinks or enlarges the image based on the smallest side of the image, with a warning if enlarging.

Command line options available with "images2resize.py --help"

### plant2caption.py

While this script may not be as useful for general images, it can be beneficial in identifying plants in close-up shots. The script utilizes the Plant Net API, for which a developer account and API key are required. A free account option is available, with a limit of up to 500 API calls per day.

Command line options available with "plant2caption.py --help"

### txts2txt.py

This script simply concatenates all text files (.txt) into one file. It can be used to create a large text document with all words in a single file.
This can help create word clouds as well as creating a summary of words used (with --dedup)

Command line options available with "txts2txt.py --help"

### txt2wordcloud.py

This script can assist in creating word clouds using tokens or text files utilized in creating captions for images. Additional examples and batch and shell scripts can be found in the examples folder.

Command line options available with "txt2wordcloud.py --help"
