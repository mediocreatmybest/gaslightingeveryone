import argparse
import os
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from PIL import Image


def create_data_row(filename, image_path, caption_path=None, caption1_path=None, caption2_path=None, url_path=None, tags_path=None):
    """ Creates a data row for a single image file."""

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

    if url_path:
        url = open_text(url_path)
    else:
        url = None

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
    # Add URL - Done.
    # Add alt text(s) and tags - Done.
    # To do: Add image hash?, finish extact script, compression? How to do that?

    # Append information to the dictionary
    row = {'file_name': filename, 'url': url, 'width': width, 'height': height,
            'text': caption, 'alt_text_a': caption1, 'alt_text_b': caption2, 'tags': tags,
            'image': image_data}
    data.append(row)
    return data


def match_image_to_text(image_files=None, text_files=None, alt_text_a_files=None, alt_text_b_files=None, url_files=None, tag_files=None):
    """ Matches image files to text files based on the file name without extension.

    Args:
        image_files (folder, optional): _description_. Defaults to None.
        text_files (folder, optional): _description_. Defaults to None.
        alt_text_a_files (folder, optional): _description_. Defaults to None.
        alt_text_b_files (folder, optional): _description_. Defaults to None.
        url_files (folder, optional): _description_. Defaults to None.
        tag_files (folder, optional): _description_. Defaults to None.

    Returns:
        list: returns matched list of dictionaries with image, text, alt_text_a, alt_text_b, url and tags
    """
    matches = []
    for image_file in image_files:
        basename = os.path.splitext(os.path.basename(image_file))[0]
        text_file = None
        alt_text_a = None
        alt_text_b = None
        url = None
        tag = None
        for file in text_files:
            if os.path.splitext(os.path.basename(file))[0] == basename:
                text_file = file
                break
        if alt_text_a_files is not None:
            for file in alt_text_a_files:
                if os.path.splitext(os.path.basename(file))[0] == basename:
                    alt_text_a = file
                    break
        if alt_text_b_files is not None:
            for file in alt_text_b_files:
                if os.path.splitext(os.path.basename(file))[0] == basename:
                    alt_text_b = file
                    break
        if url_files is not None:
            for file in url_files:
                if os.path.splitext(os.path.basename(file))[0] == basename:
                    url = file
                    break
        if tag_files is not None:
            for file in tag_files:
                if os.path.splitext(os.path.basename(file))[0] == basename:
                    tag = file
                    break
        if text_file or alt_text_a or alt_text_b or url or tag:
            matches.append({'image': image_file, 'text': text_file, 'alt_text_a': alt_text_a, 'alt_text_b': alt_text_b, 'url': url, 'tags': tag})
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
    parser.add_argument('--input-url-dir', type=str, required=False)
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
    alt_caps_folder1 = Path(args.input_captions1_dir)
if args.input_captions2_dir:
    alt_caps_folder2 = Path(args.input_captions2_dir)
if args.input_url_dir:
    url_folder = Path(args.input_url_dir)
if args.input_tags_dir:
    tags_folder = Path(args.input_tags_dir)

# Set parquet name from args
parq_name = args.parq_name

# Full save location with join
output_folder = output_folder.joinpath(parq_name)

# Image filter for file.endswith
# https://stackoverflow.com/questions/22812785/use-endswith-with-multiple-extensions
image_filter = ['.jpg', '.jpeg', '.png', '.bmp']
image_files = go_walk(image_folder, image_filter)
# Find the text files for captions, url, alt text and tags
# This might be easier if we have a naming convention for the files
# Otherwise using file extensions, suggestions?
if args.input_captions_dir:
    text_files = go_walk(captions_folder, ['.txt'])
else:
    text_files = None
if args.input_captions1_dir:
    alt_cap1 = go_walk(alt_caps_folder1, ['.txt'])
else:
    alt_cap1 = None
if args.input_captions2_dir:
    alt_cap2 = go_walk(alt_caps_folder2, ['.txt'])
else:
    alt_cap2 = None
if args.input_url_dir:
    url = go_walk(url_folder, ['.url'])
else:
    url = None
if args.input_tags_dir:
    tags = go_walk(tags_folder, ['.tags'])
else:
    tags = None

# Match the image files to the text files with function
matches = match_image_to_text(image_files, text_files, alt_cap1, alt_cap2, url, tags)

# For each match, create a data row and use match
data = []
for match in matches:
    row = create_data_row(
        filename=os.path.basename(match['image']),
        url_path=match['url'],
        image_path=match['image'],
        caption_path=match['text'],
        caption1_path=match['alt_text_a'],
        caption2_path=match['alt_text_b'],
        tags_path=match['tags']
    )
    data.extend(row)

df = pd.DataFrame(data)

# Use pyarrow to write parquet file out, added compression. I'm sure this works.
pq.write_table(pa.Table.from_pandas(df), output_folder, compression='gzip')

print('Done!, maybe..')