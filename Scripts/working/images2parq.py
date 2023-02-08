import argparse
import glob
import os
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def csv_to_parquet(csv_file, image_folder, parquet_file, recursive=True):
    """csv_to_parquet

    Args:
        csv_file (file): utf-8 csv file with headings
        image_folder (folder): folder with image structure
        parquet_file (parquet_file): outputs to parquet for storage
        rec (recursive): True or False, default True
    """
    # Load CSV to a Pandas DataFrame
    df = pd.read_csv(csv_file, header=0, encoding='utf-8', dtype=str)

    # List for image data
    image_data_list = []
    # Use globby glob glob to find images to load into dataframe
    # Can't get this to work...
    # image_ext = ('jpg', 'jpeg', 'png', 'bmp')
    # pattern = f"{image_folder}/**/*.{{{','.join(image_ext)}}}"
    pattern = f"{image_folder}/**/*.jpg"
    image_files = glob.glob(pattern, recursive=recursive)
    for image_file in image_files:
        # Get binary data
        print(image_file)
        with open (image_file, 'rb') as file:
            print(file)
            image_data = file.read()
        # Add to image_data_list
        image_data_list.append(image_data)

    # Add the image data to the Pandas DataFrame
    df['image'] = pd.Series(image_data_list)
    # Convert dataframe to pyarrow table
    table = pa.Table.from_pandas(df)
    # Write the pyarrow table to the parquet file
    print(df)
    pq.write_table(table, parquet_file)

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



# Check if output folder exists and create if not
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# Join our path and parq_name as final ouput for function
save_parq = os.path.join(output_folder, parq_name)

print('Done!, maybe..')