import argparse
import glob
import os
import shutil
from pathlib import Path

import pandas as pd
from PIL import Image
import pyarrow as pa
import pyarrow.parquet as pq


def create_data_row(filename, url, image_path, caption_path, caption1_path=None, caption2_path=None, tags_path=None):

    def open_text(path):
        with open (path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text


    with open(image_path, 'rb') as file:
        image_data = file.read()
        # Switch to PIL to get X Y dimensions
        img = Image.open(file)
        width, height = img.size

    # Collect text if it exists

    if caption_path:
        caption = open_text(caption_path)
    else:
        caption = None

    if caption1_path:
        caption1 = open_text(caption1_path)
    else:
        caption1 = None

    if caption2_path:
        caption2 = open_text(caption2_path)
    else:
        caption2 = None

    if tags_path:
        tags = open_text(tags_path)
    else:
        tags = None

    # Create data
    data = []
    # Read image information and convert to binary data - Done.
    # Add width and height using Pillow - Done.
    # Extract information from caption file - Done.
    # Add File name - Done.
    # Add URL - TO DO.
    # Add alt text(s) and tags - TO DO.
    # Append information to the dictionary
    row = {'file_name': filename, 'url': url, 'width': width, 'height': height,
            'text': caption, 'alt_text_a': caption1, 'alt_text_b': caption2, 'tags': tags,
            'image': image_data}
    data.append(row)
    return data

def match_image_to_text(image_files, text_files):
    matches = []
    for image_file in image_files:
        basename = os.path.splitext(os.path.basename(image_file))[0]
        text_file = None
        for file in text_files:
            if os.path.splitext(os.path.basename(file))[0] == basename:
                text_file = file
                break
        if text_file:
            matches.append({'image': image_file, 'text': text_file})
    return matches


def go_walk(folder, ext_filter):
    """ Walks through a folder and returns a list of files with a specific extension.

    Args:
        folder (path)
        ext (list): list of extensions to filter for

    Returns:
        list: list with full path
    """
    return [os.path.join(root, name)
            for root, dirs, files in os.walk(folder)
            for name in files
            if name.endswith(tuple(ext_filter))]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-image-dir', type=str, help='Input image directory', required=True)
    parser.add_argument('--input-captions-dir', type=str, required=True)
    parser.add_argument('--input-captions1-dir', type=str, required=False)
    parser.add_argument('--input-captions2-dir', type=str, required=False)
    parser.add_argument('--input-tags-dir', type=str, required=False)
    parser.add_argument('--output-dir', type=str, required=False)
    parser.add_argument('--parq-name', default='parquetfile.parquet', type=str, required=False)

    args = parser.parse_args()

# Set some names to make it easier to remember
if args.input_image_dir:
    image_folder = Path(args.input_image_dir)
if args.output_dir:
    output_folder = Path(args.output_dir)
if args.input_captions_dir:
    captions_folder = Path(args.input_captions_dir)
if args.input_captions1_dir:
    captions_folder1 = Path(args.input_captions1_dir)
if args.input_captions2_dir:
    captions_folder2 = Path(args.input_captions2_dir)
if args.input_tags_dir:
    tags_folder = Path(args.input_tags_dir)

# Set parquet name from args
parq_name = args.parq_name

# Image filter for file.endswith
# https://stackoverflow.com/questions/22812785/use-endswith-with-multiple-extensions
image_filter = ['.jpg', '.jpeg', '.png', '.bmp']

image_files = go_walk(image_folder, image_filter)
text_files = go_walk(captions_folder, ['.txt'])

matches = match_image_to_text(image_files, text_files)

data = []
for match in matches:
    row = create_data_row(
        filename=os.path.basename(match['image']),
        url=None,
        image_path=match['image'],
        caption_path=match['text'],
        caption1_path=None,
        caption2_path=None,
        tags_path=None
    )
    data.extend(row)

df = pd.DataFrame(data)
#pq.write_table(pa.Table.from_pandas(df), args.parq_name)

print(df)


print('Done!, maybe..')