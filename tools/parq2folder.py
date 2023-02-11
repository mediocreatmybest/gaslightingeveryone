import argparse
import os
from pathlib import Path

import pandas as pd

# Magic save function

def save_file(file_path, data, mode='w', encoding='utf-8', debug=False):
    """ Function to save a file, defaults to write mode,
    if wb is passed it will save in binary mode without encoding."""

    if not debug:
        if mode == 'wb':
            with open(file_path, mode) as f:
                f.write(data)
        elif mode == 'w':
            with open(file_path, mode, encoding=encoding) as f:
                f.write(data)
        print(f'File saved to {file_path}')
    else:
        print('Debug mode, file not saved')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract images and text from Parquet files to a folder')
    parser.add_argument('--input-parq-dir', type=str, required=True)
    parser.add_argument('--output-dir', type=str, required=True)
    args = parser.parse_args()


# Path to Parquet files from input argument
parquet_dir = Path(args.input_parq_dir)

# Create list of Parquet files, I assume all parquet files are in the same directory and end with .parquet
parquet_files = [os.path.join(parquet_dir, f) for f in os.listdir(parquet_dir) if f.endswith('.parquet')]

# For each file in the list of Parquet files
for parquet_file in parquet_files:
    # Load the Parquet file
    df = pd.read_parquet(parquet_file)

    # Loop the loop through the dataframe
    for index, row in df.iterrows():
        # Extract wanted information, need to expand this to include other columns from new arguments
        file_name = row['file_name']
        image_data = row['image']
        text = row['text']
        # To do, URL, Alt text, etc.

        # Image path and file_name for saving...
        image_file_path = os.path.join(Path(args.output_dir), file_name)
        # Call Save function
        save_file(image_file_path, image_data, mode='wb', debug=False)

        # Text file path and file_name for saving...
        text_file_path = os.path.join(Path(args.output_dir), f"{os.path.splitext(file_name)[0]}.txt")
        # Call Save function
        save_file(text_file_path, text, debug=False)