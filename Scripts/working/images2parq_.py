import argparse
import glob
import os
import shutil
from pathlib import Path

import pandas as pd
from PIL import Image
import pyarrow as pa
import pyarrow.parquet as pq


def folder_to_parquet_row(filename, url, image_path, caption_path, caption1_path=None, caption2_path=None, tags_path=None):
    """ Takes data from a folder and converts it to a row in a dataframe, that can be converted to a parquet file.

    Args:
        filename (_type_): _description_
        url (_type_): _description_
        image_binary (_type_): _description_
        image_width (_type_): _description_
        image_height (_type_): _description_
        caption (_type_): _description_
        caption1 (_type_, optional): _description_. Defaults to None.
        caption2 (_type_, optional): _description_. Defaults to None.
        caption3 (_type_, optional): _description_. Defaults to None.
        tags (_type_, optional): _description_. Defaults to None.
    """
    def open_text(path):
        with open (path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text


    with open (image_path, 'rb') as file:
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
    # Read image information and convert to binary data
    # Add width and height using Pillow
    # Extract information from caption file
    # Append information to the dictionary
    row = {'file_name': filename, 'url': url, 'width': width, 'height': height,
            'text': caption, 'alt_text_a': caption1, 'alt_text_b': caption2, 'tags': tags,
            'image': image_data}
    data.append(row)
    return data

def matching(list1, list2, list3, list4, list5):
    print('not used')

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

# Use function to toddle the files
images_path = go_walk(image_folder, image_filter)

for image in images_path:
    basename_image = os.path.basename(image)
    #print('Images: ', os.path.splitext(basename)[0])

# Caption filter, can adjust this later if more extensions are required
captions_filter = ['.txt']

captions_path = go_walk(captions_folder, captions_filter)

for caption in captions_path:
    basename_caption = os.path.basename(caption)
    #print('Text files: ', os.path.splitext(basename)[0])

test1 = 'filename.jpg'
test2 = 'http://bob.com'
test3 = 'c:\\images\\bird.jpg'
test4 = 'c:\\images\\bird.txt'


data = (folder_to_parquet_row(test1, test2, test3, test4))

df = pd.DataFrame.from_dict(data)

print(df)

# Loop images and get binary data and image size
#for image_file in images:
    # Get binary data
#    with open (image_file, 'rb') as file:
#        image_data = file.read()
    # Add to image_data_list
#    image_data_list.append(image_data)
#    width, height = PIL.Image.open(image_file).size
#    image_width.append(width)
#    image_height.append(height)
#    PIL.Image.close()

# Check if output folder exists and create if not
#if not os.path.exists(output_folder):
#    os.makedirs(output_folder)
# Join our path and parq_name as final ouput for function
#save_parq = os.path.join(output_folder, parq_name)

#df = pd.DataFrame.from_dict(data)

print('Done!, maybe..')