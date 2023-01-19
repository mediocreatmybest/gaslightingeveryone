import os
import argparse
import shutil
from PIL import Image

# Create the parser
parser = argparse.ArgumentParser(description='Copy and resize all images in a directory recursively based on the shortest side while keeping the same name')

# Set allowed images for directory scan (Sorry GIF)
image_filter = ('jpeg','jpg','png','bmp','webp')

# Add the arguments
parser.add_argument('--input-dir', metavar='c:\images', type=str, help='the input image directory path', required=True)
parser.add_argument('--output-dir', metavar='c:\images_resize', type=str, help='the image output directory path', required=True)
parser.add_argument('--keep-relative', action='store_true', default=True, help='Keep relative folder structure with output directory, on by default')
parser.add_argument('--size', metavar='576', type=int, help='desired size of the smallest side', required=True)
parser.add_argument('--copy-format', action='store_true', default=False, help='Keeps the same file format from the input image')
parser.add_argument('--format', metavar='jpg', type=str, help=f'Change the image format {image_filter}')

# Parse the arguments
args = parser.parse_args()

# Create error if copy-format is False and the format argument is None
if args.copy_format is False and args.format is None:
    raise Exception('Please select a format, use one of the following: --format or --format-copy')

# Lets create the output directory if it doesn't exist
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

# Quick jog through all files in the input directory recursively
for root, dirs, files in os.walk(args.input_dir):
    for file in files:
        # Find the base name for all files
        base_file = (os.path.splitext(file)[0])
        # Find relative path of the input directory and file
        rel_path = os.path.relpath(root, args.input_dir)
        # Apply basic image filter (Sorry GIF) we also want to be insensitive like Jann Arden
        if file.casefold().endswith(image_filter):
            # Open the image
            image = Image.open(os.path.join(root, file))

            # Get the width and height of the image
            width, height = image.size
            if args.size >= min(width, height):
                # Better way to do this? It *should* still resize and keep toddling on
                try:
                    raise ValueError((f'Beep boop! The size you specified: {args.size} is equal or larger than the source image: {file}'))
                except ValueError as err:
                    print(err)

            # Determine the new size of the image
            if width < height:
                new_size = (args.size, int(height * args.size / width))
            else:
                new_size = (int(width * args.size / height), args.size)

            # Resize the image
            resized_image = image.resize(new_size)

            # Check for copy input format (I think this works)
            if args.copy_format:
                format = image.format
                format = format.casefold()
            else:
                format = args.format
                format = format.casefold()

            # Save the resized image recursively while checking for jpeg vs jpg with its silly extension arguments
            if format == 'jpg':
                if args.keep_relative is True:
                    if args.keep_relative is True:
                        output_path = (os.path.join(args.output_dir, rel_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    resized_image.save(os.path.join(output_path, base_file + '.jpg'), 'jpeg')
                else:
                    resized_image.save(os.path.join(args.output_dir, base_file + '.jpg'), 'jpeg')

            if args.copy_format is False and format != 'jpg':
                if args.keep_relative is True:
                    output_path = (os.path.join(args.output_dir, rel_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    resized_image.save(os.path.join(output_path, base_file + '.'+format), format)
                else:
                    resized_image.save(os.path.join(args.output_dir, base_file + '.'+format), format)

            if args.copy_format:
                if args.keep_relative is True:
                    if args.keep_relative is True:
                        output_path = (os.path.join(args.output_dir, rel_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    resized_image.save(os.path.join(output_path, file), format)
                else:
                    resized_image.save(os.path.join(args.output_dir, file), format)

            # Check if the image file as a matching text file and copy to new directory
            text_file = base_file + '.txt'

            if args.keep_relative is True:
                output_path = (os.path.join(args.output_dir, rel_path))
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                if os.path.exists(os.path.join(root, text_file)):
                # If it exists, copy it
                    shutil.copy2(os.path.join(root, text_file), os.path.join(output_path, text_file))
            else:
                if os.path.exists(os.path.join(root, text_file)):
                    # If it exists, copy it
                    shutil.copy2(os.path.join(root, text_file), os.path.join(args.output_dir, text_file))