import argparse
import json
import os
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

# Use main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, required=True)
    args = parser.parse_args()
    # Set input string as a Path object
    image_captions_path = Path(rf"{args.input_dir}")

# Find all JSON files in the directory
    json_files = list(image_captions_path.glob('**/*.json'))

    for json_file in tqdm(json_files, desc="Dump URLs", unit="dump2url"):
        # Parent Folder
        parent_folder = Path(json_file.parent.as_posix())
        # json filename
        filename = Path(json_file.as_posix())
        # Get base name of json file without extension
        # Need to use with_suffix for this
        basename = filename.with_suffix('').stem
        # Load json file
        jsondata = json.loads(filename.read_text(encoding='utf-8'))
        urls = json_extract(jsondata, 'url')
        if urls:
            # Do something else here. Maybe save the url to a file...
            print(filename, urls[0])


