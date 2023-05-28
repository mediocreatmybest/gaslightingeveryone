# Caption Scripts

## Caption creation tools

These scripts/tools have been made to assist in the creation of captions for programs such as stable diffusion, utilising existing metadata (from gallery-dl downloads) or editing text files in bulk, or using BLIP/CLIP to help create them.
All the main tools and scripts are located in the tools folder.

Any issues please help by: fixing and pulling, otherwise please create an issue and make suggestions or point me in a better direction.

### captions2generate.py

This is aimed at being a fairly simple captioning script by using pipeline() to do the heavy lifting with Transformers to create a task using supported models for captions and image categories with the zero-shot task. This seems to have made it flexible enough to run BLIP2 6.7 billion parameters (Salesforce/blip2-opt-6.7b) on the CPU if you have about 32GB of RAM. It isn't the most efficent script, but it works. Please see requirements_captions2generate.txt for the requirements.

#### Usage

At a minimum you need to select a caption model or CLIP model to use:
For example:
`python captions2generate.py /path/to/directory --model blip-large`

```bash
`<directory>`: The directory to search for images.
`--depth`: Sets how deep to travel into folders (optional).
`--mode`: Sets the write mode to use when existing captions are found (optional, default: 'write').
`--skip-existing`: Skip existing files if found (optional).
`--ext`: Extension for the caption files (optional, default: 'txt' or 'caption').
`--cpu-offload`: Switches to CPU (optional), <-- This may let you run BLIP2 if you have enough system RAM.
`--model`: Model to use for image captioning (optional, choose from available models).
`--clip-model`: Model to use for CLIP/Zero Shot Category (optional, choose from available models).
`--clip-cat-text`: File containing CLIP/Zero Shot Category labels (optional).
`--clip-confidence`: Categories under the confidence score won't be included in the final text output (optional, default: 0.70).
`--max-tokens`: The maximum number of tokens for the caption model (optional, default: 25).
`--batch-count`: If you want to try larger than batch size of 1, image with image batch count with pipeline captions (optional).
`--quiet`: Suppresses caption output (optional).
```

The script will process the images in the specified directory and generate captions based on the selected models. The captions will be saved in separate text files.
When using --clip-model you will need to provide a list of image categories with --clip-cat-text, see example folder, create your own, or grab some from other projects. Just make sure they aren't too large, for example flavours.txt from clip-interrogator is too large for this poor little script.

### json2txt.py

This script can assist in gathering captions from websites that provide useful information such as titles, descriptions, alt descriptions, EXIF data, and tags for media collected using gallery-dl, to generate metadata files (e.g., gallery-dl --write-metadata). The script takes input from a useful, yet randomly organized JSON file and creates a text file with the same name, as well as an appended file.

The contents of the file will be: *Title, Description, Alt_Description, EXIF data, Tags*

As an example: *The Fat Cat Barnaby, Barnaby is always very sleepy and looks drunk, ISO: 200, Focal Length: 100.0, Model is NIKON D850, Aperture: 4.5, Fat Cat, Lazy, sleeping*

The text file will only include elements present in the JSON file, if the JSON is missing any of the following information: title, description, Alt_Description, EXIF, or tags, they will not be included in the text file.

Command line options available with ```"json2txt.py --help"```

### json2caption.py

json2caption.py is a script that can help create captions for your images by collecting all the values from the json metadata that was downloaded or created with the images, including headings, and creating a plain text file (txt, tags, caption). It also includes a word swap feature to replace certain words with others using a basic text file.

#### Usage is more complex than I'd have liked but here we are

Use the script on json files that contain image metadata *(from programs such as gallery-dl)*, a simple example command:

```json2caption.py "/image/directory or c:\images\images" --filter "tags: " --keys "tags"* *(Note the spaces you wish to filter)```

This will create a file in the same directory with .tags by default.

For json files with a less standard structure, you can use additional filter files, you have the option of simple replacement filter or regex.

```json2caption.py "/image/directory or c:\images\images" --filter-file "filter_file.txt" --word-swap "word_swap_dictionary.txt" --keys "tags"```

The filter_file.txt is a Python regex and each new line is a new filter. The word_swap_dictionary is a simple dictionary file with words separated by a |-|
Each new line is a new word swap filter. See the examples in the [filter_files folder](https://github.com/mediocreatmybest/gaslightingeveryone/tree/main/examples/filter_files)

The only required argument is the directory, but more than likely you would want to filter the results.
The current arguments available are:

```bash
--write-mode: how to treat existing data if found. The default value is 'write' this will overwrite existing files, but it can be set to 'append' or 'prepend'.
--keys: A comma-separated list of keys or values to collect. The default value is 'tags'.
--tag-keys: If the original data is separated by spaces, this argument specifies the values that should be treated as separate tags.
--order-by: A comma-separated list of keys that allows you to change the order of the output.
--output-file: The name of the output file. Useful if you wish to save a single file
--output-folder: The folder to save the output file in. Useful if you wish to save in an alternative folder or for testing.
--output-extension: The extension of the output file. The default value is 'tags', but it can also be set to 'txt' or 'caption'.
--filter: A comma-separated list of text patterns to remove from the output. This argument accepts regex.
--filter-file: An alternative list of text patterns to remove from the output. Each new line is a separate filter. This argument only filters JSON values.
--regex-filter-file: An alternative regex list of text patterns to remove from the output. Each new line is a separate filter. This argument only filters JSON values.
--word-swap: A text file with a pipe dash pipe |-| separated word swap pairs. This argument is useful for unwanted key values, and it only swaps JSON values.
--underscore-to-space: Converts underscores to spaces in the output. The default value is 'yes', but it can be set to 'no'.
--debug: Disables saving files, prints output, and shows the save location.
```

#### Subkeys in JSON file

Subkeys can be selected independently of the primary key. This is particularly useful when the primary key contains additional subkeys that are not relevant or contain unwanted values.

To select a subkey on its own, use the following command:

```bash
--keys primarykey.subkey
```

If you need to filter subkeys, you must use its full key name.
The filtering process works in the same way as with primary keys, including the ability to swap words.

#### Notes

This script has been made to fix some issues with the initial json2txt.py script. While it may be elaborate for something that could have been done in a simpler way, it aims to provide a more comprehensive way to help create captions for images from existing data, or break at the drop of a hat.
Does anyone read this? Am I so out of touch? No...it's the others who are wrong.

### captions2merge.py

captions2merge.py can be used to merge captions from image files into a single plain text file.

To use the script, specify the input directory containing the image files using the --input-dir option. By default, the script will merge .caption and .tags files together to create image1.txt. You can also select any plain text file to merge.

e.g.

'''captions2merge.py --input-dir "/images/ or C:\images"'''

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

- Multiples Crop (--multiples-crop): Crops the edges of an image to the closest multiple of a specified number of pixels (e.g. 64 pixels for a 1024x768 image).
- Aspect Ratio Crop (--aspect-crop): Crops the image to the closest specified aspect ratio (1,1.33,1.5,etc.), but wil not enlarge the image.
- Resize on Small Side *(I'm sure this could have a better name)* (--resize-small-side): Shrinks or enlarges the image based on the smallest side of the image, with a warning if enlarging.

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
