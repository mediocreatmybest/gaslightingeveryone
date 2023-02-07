import argparse
import glob

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def csv_to_parquet(csv_file, image_folder, parquet_file):
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

    # Get all images via glob, yep. globby glob glob.
    # Switch this to get more images. *** FIX ME ***
    image_files = glob.glob(f'{image_folder}/**/*.jpg', recursive=True)
    for image_file in image_files:
        # Get binary data
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
    parser.add_argument('--input-dir', type=str, required=False)
    parser.add_argument('--input-csv', type=str, required=False)
    parser.add_argument('--parq-name', default='parquetfile.parquet', type=str, required=False)


    args = parser.parse_args()

image_folder = args.input_dir
input_csv = args.input_csv
parq_name = args.parq_name
# Use globby glob glob to find images to load into dataframe
image_files = glob.glob(f"{image_folder}/**/*.{'jpg','jpeg','png','bmp'}", recursive=True)

csv_to_parquet(csv_file=input_csv, image_folder=image_folder, parquet_file=parq_name)
print('Done!, maybe..')