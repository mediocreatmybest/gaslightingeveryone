import argparse
import glob
import os
import shutil
from pathlib import Path

import pandas as pd
import PIL
import pyarrow as pa
import pyarrow.parquet as pq


def folder_to_parquet_row(filename, url, image_binary, image_width, image_height, captions, captions1=None, captions2=None, captions3=None, tags=None):
    """ Takes data from a folder and converts it to a row in a dataframe, that can be converted to a parquet file.

    Args:
        filename (_type_): _description_
        url (_type_): _description_
        image_binary (_type_): _description_
        image_width (_type_): _description_
        image_height (_type_): _description_
        captions (_type_): _description_
        captions1 (_type_, optional): _description_. Defaults to None.
        captions2 (_type_, optional): _description_. Defaults to None.
        captions3 (_type_, optional): _description_. Defaults to None.
        tags (_type_, optional): _description_. Defaults to None.
    """

    # Create data
    data = []
    # Read image information and convert to binary data
    # Add width and height using Pillow
    # Extract information from caption file
    # Append information to the dictionary
    row = {'file_name': filename, 'url': url, 'width': image_width, 'height': image_height,
            'text': captions, 'alt_text_a': captions1, 'alt_text_b': captions2, 'alt_text_c': captions3,
            'tags': tags, 'image': image_binary}
    data.append(row)

#df = pd.DataFrame.from_dict(data)


#image_base = os.path.basename(image)
#caption_base = os.path.basename(captions)

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
    parser.add_argument('--input-dir', type=str, help='Input image directory', required=True)
    parser.add_argument('--input-captions-dir', type=str, required=False)
    parser.add_argument('--input-captions1-dir', type=str, required=False)
    parser.add_argument('--input-captions2-dir', type=str, required=False)
    parser.add_argument('--input-captions3-dir', type=str, required=False)
    parser.add_argument('--output-dir', type=str, required=False)
    parser.add_argument('--parq-name', default='parquetfile.parquet', type=str, required=False)

    args = parser.parse_args()

# Set some names to make it easier to remember
image_folder = Path(args.input_dir)
#output_folder = Path(args.output_dir)
captions_folder = Path(args.input_captions_dir)
#captions_folder1 = Path(args.input_captions1_dir)
#captions_folder2 = Path(args.input_captions2_dir)
#captions_folder3 = Path(args.input_captions3_dir)

# Set parquet name from args
parq_name = args.parq_name

# Image filter for file.endswith
# https://stackoverflow.com/questions/22812785/use-endswith-with-multiple-extensions
image_filter = ['.jpg', '.jpeg', '.png', '.bmp']

images = []
# Find required files
#for root, dirs, files in os.walk(image_folder):
#    for file in files:
#        if file.endswith(tuple(image_filter)):
#            # Full directory path
#            full_directory = root
#            # Full path including file
#            full_path = os.path.join(root, file)
#            # Filename
#            image_basename = os.path.basename(file)
#            # Filename with removed extension for matching
#            #image_match = image_basename.split('.')[0]
#            # Alternative extension removal
#            image_match = os.path.splitext(image_basename)
#            #images.append(full_path)

#for image in images:
#    basename = os.path.basename(image)
#    print(os.path.splitext(basename)[0])

images_path = go_walk(image_folder, image_filter)

#for image in images_path:
#    basename = os.path.basename(image)
#    print(os.path.splitext(basename)[0])

captions_filter = ['.txt']
captions = []
captions_path = go_walk(captions_folder, captions_filter)

for caption in captions_path:
    basename = os.path.basename(caption)
    print(os.path.splitext(basename)[0])


#images = []
#for files in image_pattern:
#    image_file = glob.glob(files)
#    images += image_file
#print(images)

#captions = []
#for caption in caption_pattern:
#    caption_file = glob.glob(caption)
#    captions += caption_file
#print(captions)

#captions1 = []
#for caption1 in caption_pattern1:
#    caption_file1 = glob.glob(caption1)
#    captions1 += caption_file1
#print(captions1)



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

print('Done!, maybe..')