import os
import random
import string
import argparse

parser = argparse.ArgumentParser(description="Generate a number of files with random names and extensions")
parser.add_argument("-n", "--number-of-files", type=int, default=10000, help="number of files to create")
parser.add_argument("-i", "--input-folder", type=str, default="C:/MyFolder", help="Folder path to generate files")
args = parser.parse_args()

# number of files to create
number_of_files = args.number_of_files

# path of the folder to create
folder_path = args.input_folder

# create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Create files
for i in range(number_of_files):
    # Generate random file name and extension
    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    file_extension = ''.join(random.choices(string.ascii_letters, k=random.randint(1, 3)))

    # Join file name, extension, and folder path
    file_path = os.path.join(folder_path, f"{file_name}.{file_extension}")

    # Create the folder if it doesn't exist
    file_folder = os.path.dirname(file_path)
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    # Create the file with 1 byte of useless content
    with open(file_path, 'wb') as f:
        f.write(b'\x00')

    # Output the file path
    print(f"Beep! Boop! created file at {file_path}")
