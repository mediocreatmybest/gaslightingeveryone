import os
import argparse
from PIL import Image

# Create the parser
parser = argparse.ArgumentParser(description='Copy and resize all images in a directory recursively based on the shortest side while keeping the same name')

# Set allowed images for directory scan (Sorry GIF)
image_filter = ('jpeg','jpg','png','bmp')

# TODO: Copy caption files

# Add the arguments
parser.add_argument('--input-dir', metavar='c:\images', type=str, help='the input image directory path', required=True)
parser.add_argument('--output-dir', metavar='c:\images-smaller', type=str, help='the image output directory path', required=True)
parser.add_argument('--size', metavar='576', type=int, help='desired size of the smallest side', required=True)

# Parse the arguments
args = parser.parse_args()

# Lets create the output directory if it doesn't exist
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

# Quick jog through all files in the input directory recursively
for root, dirs, files in os.walk(args.input_dir):
    for file in files:
        # Apply basic image filter (Sorry GIF)
        if file.casefold().endswith(image_filter):
            # Open the image
            image = Image.open(os.path.join(root, file))

            # Get the width and height of the image
            width, height = image.size
            if args.size >= min(width, height):
                raise ValueError(f"The size you specified: {args.size} is too big. *cough* sorry. It should be smaller than the existing image: {file}")

            # Determine the new size of the image
            if width < height:
                new_size = (args.size, int(height * args.size / width))
            else:
                new_size = (int(width * args.size / height), args.size)

            # Resize the image
            resized_image = image.resize(new_size)

            # Save the resized image recursivily (hopefully)
            resized_image.save(os.path.join(args.output_dir, file))