import os
import random
import string

# Define the number of files to create
number_of_files = 10000

# Define the path of the folder to create
folder_path = "C:/MyFolder"

# Create the folder if it doesn't already exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Generate and create the files
for i in range(number_of_files):
    # Generate a random file name
    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    # Combine the file name and folder path to create the full file path
    file_path = os.path.join(folder_path, file_name)

    # Create the file with 1 byte of content
    with open(file_path, 'wb') as f:
        f.write(b'\x00')

    # Output the file path for logging purposes
    print(f"Created file {file_path}")