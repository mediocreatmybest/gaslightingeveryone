import pandas as pd
import argparse
import os

# Create the arg parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--imagedir', type=str, help='Image directory to caption', metavar='c:\images', required=True)

# Parse the argument
args = parser.parse_args()

folder_path = args.imagedir



# Initialize empty lists to store the filenames and captions
image_filenames = []
captions = []

# Loop through the files in the folder
for file in os.listdir(folder_path):
    # Check if the file is an image
    if file.endswith('.jpg') or file.endswith('.png'):
        # Find basename of the image files
        basename = (os.path.splitext(file)[0])
        txtfile = basename + '.txt'
        # Add the image filename to the list
        image_filenames.append(file)



    # Check if the file is a caption file
    elif file.endswith('.txt'):
        # Open the caption file and read the caption
        with open(os.path.join(folder_path, file), 'r') as f:
            caption = f.read()
        # Add the caption to the list
        captions.append(caption)

# Combine the lists into a single list of tuples
data = list(zip(image_filenames, captions))

# Create a Pandas dataframe from the list of tuples
df = pd.DataFrame(data, columns=['image', 'caption'])

# Print the first 5 rows of the dataframe
print(df.head())



# Access the image filenames and captions
image_filenames = df['image']
captions = df['caption']