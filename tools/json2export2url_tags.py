import argparse
import json
import os
import sys
from pathlib import Path

from tqdm import tqdm

def json_extract(obj, key):
    """ Recursively fetch values from nested JSON:
        See: https://hackersandslackers.com/extract-data-from-complex-json-python/
    """
    arr = []

    def extract(obj, arr, key):
        """ Recursively search for values of key in JSON tree """
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

def list2String(convertlist):
    """initialize a list into separated string"""
    # Check if tags are separated by comma or space
    if all("," in tag for tag in convertlist):
        separator = ", "
    else:
        separator = " "
    # Return string
    return separator.join(convertlist)


def save_file(file_path, data, mode='w', encoding='utf-8', debug=False):
    """ Function to save a file, defaults to write mode """
    if not debug:
        with open(file_path, mode, encoding=encoding) as f:
            f.write(data)
        print(f'File saved to {file_path}')
    else:
        print('Debug mode, file not saved')

# Use main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, required=True)
    parser.add_argument('--export-urls', action='store_true', required=False)
    parser.add_argument('--export-tags', action='store_true', required=False)
    args = parser.parse_args()
    # Set input string as a Path object
    image_captions_path = Path(rf"{args.input_dir}")

    # Check if export type is selected
    # If both arguments are not set, exit
    if not args.export_urls and not args.export_tags:
        print('Please select an option to export --export-tags, --export-urls')
        sys.exit()


# Find all JSON files in the directory
    json_files = list(image_captions_path.glob('**/*.json'))
    # For each file via globy
    for json_file in tqdm(json_files, desc="Extract json keys", unit=" keys"):
        # Parent Folder
        parent_folder = Path(json_file.parent.as_posix())
        # json filename
        filename = Path(json_file.as_posix())
        # Get base name of json file without extension
        # Need to use with_suffix for this
        basename = filename.with_suffix('').stem
        # Load json file
        jsondata = json.loads(filename.read_text(encoding='utf-8'))
        jsonkeys = json_extract(jsondata, 'url')

        if args.export_tags is True:
            if "tags" in jsondata:
                tags = jsondata['tags']
                # Check if tags are a string or list
                if isinstance(tags, str):
                    tags = tags.split()
                tagstr = list2String(tags)
                # Export tags to file
                tagsfullpath = os.path.join(parent_folder, basename + '.tags')
                save_file(tagsfullpath, tagstr, debug=False)


        if args.export_urls is True:
            if jsonkeys:
                # Do something else here. Maybe save the jsonkey to a file...
                keyfullpath = os.path.join(parent_folder, basename + '.url')
                save_file(keyfullpath, jsonkeys[0], debug=False)