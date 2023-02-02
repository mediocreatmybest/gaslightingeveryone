import argparse
import os
import shutil
from multi_crop_func2 import *

from PIL import Image

# Create the parser
parser = argparse.ArgumentParser(description='Copy, crop, and resize all images in a directory recursively')

# Set allowed images for directory scan (Sorry GIF)
image_filter = ('jpeg','jpg','png','bmp','webp')

# Add the arguments
parser.add_argument('--input-dir', metavar='c:\images', type=str,
                    help='the input image directory path', required=True)
parser.add_argument('--output-dir', metavar='c:\images_resize', type=str,
                    help='the image output directory path', required=True)
parser.add_argument('--keep-relative', action='store_true', default=True,
                    help='Keep relative folder structure with output directory, on by default')
parser.add_argument('--copy-format', action='store_true', default=False,
                    help='Keeps the same file format from the input image')
parser.add_argument('--format', metavar='jpg', type=str,
                    help=f'Change the image format {image_filter}')
parser.add_argument('--multiples-crop', action='store_true', default=False,
                    help='Crops the image to the closest specified multiple')
parser.add_argument('--multiples-of', metavar='64', default=64, type=int,
                    help='Desired image size in multiples of pixel count e.g 64', required=False)
parser.add_argument('--aspect-crop', action='store_true', default=False,
                    help='Desired aspect ratios for the closest crop')
#parser.add_argument('--aspect-ratios', type=str, default='1:1,1:2,2:1,3:4,4:3,9:16,16:9,21:9',
#                    help='Set desired aspect ratios in comma seperated list e.g 1:1,4:3')
parser.add_argument('--aspect-ratios', type=str, default='0.56,0.75,0.8,1,1.33,1.5,1.6,1.78', # What are the most reliable and needed ratios?
                    help='Set desired aspect ratios as a float in comma seperated list e.g 0.56,0.75,0.8,1,1.33,1.5,1.6,1.78')
parser.add_argument('--resize-small-side', action='store_true', default=False,
                    help='Resizes to the specified min_size while keeping the aspect ratio')
parser.add_argument('--min-size', metavar='768', type=int,
                    help='desired size of the smallest side', required=False)
parser.add_argument('--debug', action='store_true', default=False,
                    help='Print debug messages of output images', required=False)



# Parse the arguments
args = parser.parse_args()

# Create error if resize and crop options are all False aka not used
if args.aspect_crop is False and args.resize_small_side is False and args.multiples_crop is False:
    raise Exception('Please select a resize method, use one of the following: --aspect-crop, --resize-small-side, --multiples-crop')

# Create error if copy-format is False and the format argument is None
# I suspect this should just be removed and --copy-format should be enabled by default?
if args.copy_format is False and args.format is None:
    raise Exception('Please select a format, use one of the following: --format or --copy-format')

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
            # Open the image to get format
            image = Image.open(os.path.join(root, file))
            # Set full path for functions
            #fullpath = os.path.join(root, file)

            if args.debug is True:
                print('Image file is: ', file)
                print('Original Image size: ', image.size)

                # Use the resize_to_min function from multi_crop_func.py
                # This should be done before any other silly resizing is done

            if args.resize_small_side is True:
            # As we didn't set a default for min_size we need to check for it
                if args.min_size is None:
                    raise Exception('Please select the minimum size, use the following: --min-size')
                else:
                    img = resize_small_side(image, args.min_size)
                    if args.debug is True:
                        print(f'Multiple Crop is: {(args.multiples_crop)}')
                        print(f'Aspect Crop is: {(args.aspect_crop)}')
                        print(f'Resize on small size is: {(args.resize_small_side)}')
                        print('Resize on small side size: ', img.size)
                        print('Min_size was set to: ', args.min_size)

            # Use the crop_to_multiple function from multi_crop_func.py
            # As we need to strip the image of these pixels first to maintain a useful image
            # This function should probably be done on its own
            if args.multiples_crop is True:
                if args.resize_small_side is True:
                    img = crop_to_multiple(img, args.multiples_of)
                    if args.debug is True:
                        print(f'Multiple Crop is: {(args.multiples_crop)}')
                        print(f'Aspect Crop is: {(args.aspect_crop)}')
                        print(f'Resize on small size is: {(args.resize_small_side)}')
                        print('Output of multiples_crop size: ', img.size)
                else:
                    img = crop_to_multiple(image, args.multiples_of)
                    if args.debug is True:
                        print(f'Multiple Crop is: {(args.multiples_crop)}')
                        print(f'Aspect Crop is: {(args.aspect_crop)}')
                        print(f'Resize on small size is: {(args.resize_small_side)}')
                        print('Output of multiples_crop size: ', img.size)

            # Use the crop_to_aspect function from multi_crop_func.py
            # As we need to maintain x:y aspect ratio to keep multiples of arguments
            if args.aspect_crop is True:
                if args.multiples_crop is True or args.resize_small_side is True:
                    img = crop_to_set_aspect_ratio(img, args.aspect_ratios, debug=args.debug)
                    if args.debug is True:
                        print(f'Multiple Crop is: {(args.multiples_crop)}')
                        print(f'Aspect Crop is: {(args.aspect_crop)}')
                        print(f'Resize on small size is: {(args.resize_small_side)}')
                        print('Output of aspect_crop size: ', img.size)
                else:
                    img = crop_to_set_aspect_ratio(image, args.aspect_ratios, debug=args.debug)
                    if args.debug is True:
                        print(f'Multiple Crop is: {(args.multiples_crop)}')
                        print(f'Aspect Crop is: {(args.aspect_crop)}')
                        print(f'Resize on small size is: {(args.resize_small_side)}')
                        print('Output of aspect_crop size: ', img.size)


            # Check for copy input format (I think this works)
            if args.copy_format:
                format = img.format
            else:
                format = args.format

            # Save the resized image recursively while checking for jpeg vs jpg with its silly extension arguments
            if format == 'jpg':
                if args.keep_relative is True:
                    if args.keep_relative is True:
                        output_path = (os.path.join(args.output_dir, rel_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    img.save(os.path.join(output_path, base_file + '.jpg'), 'jpeg')
                else:
                    img.save(os.path.join(args.output_dir, base_file + '.jpg'), 'jpeg')

            if args.copy_format is False and format != 'jpg':
                if args.keep_relative is True:
                    output_path = (os.path.join(args.output_dir, rel_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    img.save(os.path.join(output_path, base_file + '.'+format), format)
                else:
                    img.save(os.path.join(args.output_dir, base_file + '.'+format), format)

            if args.copy_format:
                if args.keep_relative is True:
                    if args.keep_relative is True:
                        output_path = (os.path.join(args.output_dir, rel_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    img.save(os.path.join(output_path, file), format)
                else:
                    img.save(os.path.join(args.output_dir, file), format)

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