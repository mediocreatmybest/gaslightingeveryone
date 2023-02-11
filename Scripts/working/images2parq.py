import argparse
import glob
import os
import PIL
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def folder_to_parquet_row(filename, images, captions, captions1=None, captions2=None, captions3=None):

    print('Not implemented yet')

    data = []
    for image, caption in zip(images, captions, captions1, captions2, captions3):
        image_base = os.path.basename(image)
        caption_base = os.path.basename(caption)

    if image_base == caption_base:
        # Read image information and convert to binary data
        # Add width and height using Pillow
        # Extract information from caption file
        # Append information to the dictionary
        row = {'file_name': filename, 'url': url, 'width': width, 'height': height,
               'text': captions, 'alt_text_a': captions1, 'alt_text_b': captions2, 'alt_text_c': captions3,
               'tags': tags, 'image': image_binary}
        data.append(row)

#df = pd.DataFrame.from_dict(data)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Input image directory', required=True)
    parser.add_argument('--input-captions-dir', type=str, required=True)
    parser.add_argument('--input-captions1-dir', type=str, required=False)
    parser.add_argument('--input-captions2-dir', type=str, required=False)
    parser.add_argument('--input-captions3-dir', type=str, required=False)
    parser.add_argument('--output-dir', type=str, required=True)
    parser.add_argument('--parq-name', default='parquetfile.parquet', type=str, required=False)

    args = parser.parse_args()

# Set some names to make it easier to remember
image_folder = Path(args.input_dir)
output_folder = Path(args.output_dir)
captions_folder = Path(args.input_captions_dir)
captions_folder1 = Path(args.input_captions1_dir)
captions_folder2 = Path(args.input_captions2_dir)
captions_folder3 = Path(args.input_captions3_dir)

# Set parquet name from args
parq_name = args.parq_name

# Find required files
# Example from: https://www.adamsmith.haus/python/answers/how-to-get-a-list-of-multiple-file-types-in-a-directory-using-the-glob-module-in-python
image_pattern = [f"{image_folder}/**/*.jpg", f"{image_folder}/**/*.jpeg", f"{image_folder}/**/*.png", f"{image_folder}/**/*.bmp",]
caption_pattern = [f"{captions_folder}/**/*.txt"]
caption_pattern1 = [f"{captions_folder}/**/*.txt"]

images = []
for files in image_pattern:
    image_file = glob.glob(files)
    images += image_file
print(images)

captions = []
for caption in caption_pattern:
    caption_file = glob.glob(caption)
    captions += caption_file
print(captions)

captions1 = []
for caption1 in caption_pattern1:
    caption_file1 = glob.glob(caption1)
    captions1 += caption_file1
print(captions1)

# List for image data
image_data_list = []
image_width = []
image_height = []

# Loop images and get binary data and image size
for image_file in images:
    # Get binary data
    with open (image_file, 'rb') as file:
        image_data = file.read()
    # Add to image_data_list
    image_data_list.append(image_data)
    width, height = PIL.Image.open(image_file).size
    image_width.append(width)
    image_height.append(height)
    PIL.Image.close()

# Check if output folder exists and create if not
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# Join our path and parq_name as final ouput for function
save_parq = os.path.join(output_folder, parq_name)

print('Done!, maybe..')