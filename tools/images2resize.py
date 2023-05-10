import argparse
import os
import shutil

from PIL import Image

from func_image import (check_trans_background, crop_to_multiple,
                             crop_to_set_aspect_ratio, pad_to_1_to_1,
                             replace_trans_background, resize_side_size)

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
parser.add_argument('--aspect-ratios', type=str, default='0.56,0.75,0.8,1,1.33,1.5,1.6,1.78', # What are the most reliable and needed ratios?
                    help='Set desired aspect ratios as a float in comma seperated list e.g 0.56,0.75,0.8,1,1.33,1.5,1.6,1.78')
parser.add_argument('--resize', action='store_true', default=False,
                    help='Resizes (based on shortest side) to the specified min_size while keeping the aspect ratio')
parser.add_argument('--resize-mode', type=str, default='smallest',
                    help='Resize modes: smallest (resizes based on smallest side of image), largest (resizes on largest side of image)',
                    choices=['smallest', 'largest'], required=False)
parser.add_argument('--min-size', metavar='768', type=int,
                    help='desired size of the smallest side', required=False)
parser.add_argument('--pad-image', action='store_true', default=False,
                    help='Pads the image to a 1:1 ratio')
parser.add_argument("-c", "--color", type=str,
                    help="Manually specify a colour for transparent background replacement (format: R,G,B).")
parser.add_argument("--common-colors", action="store_true",
                    help="Use a limited number of simple background colours for transparent ground replacement")
parser.add_argument('--debug', action='store_true', default=False,
                    help='Print debug messages of output images', required=False)

# Parse the arguments
args = parser.parse_args()

# Create error if resize and crop options are all False aka not used
if args.aspect_crop is False and args.resize is False and args.multiples_crop is False and args.pad_image is False:
    raise Exception('Please select a resize method, use one of the following: --aspect-crop, --resize-small-side, --multiples-crop --pad-image')

# Create error if copy-format is False and the format argument is None
# I suspect this should just be removed and --copy-format should be enabled by default?
if args.copy_format is False and args.format is None:
    raise Exception('Please select a format, use one of the following: --format or --copy-format')

# Convert the string to a list of floats
# Will it be better to use the X:Y function or keep floating point?
aspect_ratios_split = [float(x) for x in args.aspect_ratios.split(',')]
aspect_ratios = [x for x in aspect_ratios_split]

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

                # Use the resize_side_size function from multi_crop_func.py
                # This should be done before any other of my silly resizing functions

            if args.resize is True:
            # As we didn't set a default for min_size we need to check for it
                if args.min_size is None:
                    raise Exception('Please select the minimum size, use the following: --min-size')
                else:
                    img = resize_side_size(image, args.min_size, args.resize_mode)
                    if args.debug is True:
                        print(f'Multiple Crop is: {(args.multiples_crop)}')
                        print(f'Aspect Crop is: {(args.aspect_crop)}')
                        print(f'Resize mod is: {(args.resize)}')
                        print('Resize size: ', img.size)
                        print('Min_size was set to: ', args.min_size)

            # Use the crop_to_multiple function from multi_crop_func.py
            # As we need to strip the image of these pixels first to maintain a useful image
            # This function should probably be done on its own
            if args.multiples_crop is True:
                if args.resize is True:
                    img = crop_to_multiple(img, args.multiples_of)
                    if args.debug is True:
                        print(f'Multiple Crop is: {(args.multiples_crop)}')
                        print(f'Aspect Crop is: {(args.aspect_crop)}')
                        print(f'Resize mod is: {(args.resize)}')
                        print('Output of multiples_crop size: ', img.size)
                else:
                    img = crop_to_multiple(image, args.multiples_of)
                    if args.debug is True:
                        print(f'Multiple Crop is: {(args.multiples_crop)}')
                        print(f'Aspect Crop is: {(args.aspect_crop)}')
                        print(f'Resize mod is: {(args.resize)}')
                        print('Output of multiples_crop size: ', img.size)

            # Use the crop_to_aspect function from multi_crop_func.py
            # As we need to maintain x:y aspect ratio to keep multiples of arguments
            if args.aspect_crop is True:
                if args.multiples_crop is True or args.resize is True:
                    img = crop_to_set_aspect_ratio(img, aspect_ratios, debug=args.debug)
                    if args.debug is True:
                        print(f'Multiple Crop is: {(args.multiples_crop)}')
                        print(f'Aspect Crop is: {(args.aspect_crop)}')
                        print(f'Resize mod is: {(args.resize)}')
                        print('Output of aspect_crop size: ', img.size)
                else:
                    img = crop_to_set_aspect_ratio(image, aspect_ratios, debug=args.debug)
                    if args.debug is True:
                        print(f'Multiple Crop is: {(args.multiples_crop)}')
                        print(f'Aspect Crop is: {(args.aspect_crop)}')
                        print(f'Resize mode is: {(args.resize)}')
                        print('Output of aspect_crop size: ', img.size)

            # Use Pad function from multi_crop_func.py
            # Basic padding to move an image to a 1:1 aspect ratio
            # Need to add debug
            if args.pad_image is True:
                if args.resize is True:
                    img = pad_to_1_to_1(img)
                else:
                    img = pad_to_1_to_1(image)

            # Add some options to check and remove alpha or transparent backgrounds with PIL
            # If replace transparent background with common colors is selected, replace with basic 9 colours
            if args.common_colors is True:
                if check_trans_background(img) is True:
                    img = replace_trans_background(img, common_colors=args.common_colors)

            if args.color:
                specified_color = tuple(map(int, args.color.split(",")))
                if check_trans_background(img) is True:
                    img = replace_trans_background(img, specified_color=specified_color)

            # Check for copy input format (I think this works)
            if args.copy_format:
                format = img.format
            else:
                format = args.format

            # Set default quality for jpg and webp (95), add to argparse later
            quality = 95

            # Save the resized image recursively while checking for jpeg vs jpg with its silly extension arguments
            if format == 'jpg':
                if args.keep_relative is True:
                    if args.keep_relative is True:
                        output_path = (os.path.join(args.output_dir, rel_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    img.save(os.path.join(output_path, base_file + '.jpg'), 'jpeg', quality=quality)
                else:
                    img.save(os.path.join(args.output_dir, base_file + '.jpg'), 'jpeg', quality=quality)

            if args.copy_format is False and format != 'jpg':
                if args.keep_relative is True:
                    output_path = (os.path.join(args.output_dir, rel_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    img.save(os.path.join(output_path, base_file + '.'+format), format, quality=quality)
                else:
                    img.save(os.path.join(args.output_dir, base_file + '.'+format), format, quality=quality)

            if args.copy_format:
                if args.keep_relative is True:
                    if args.keep_relative is True:
                        output_path = (os.path.join(args.output_dir, rel_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    img.save(os.path.join(output_path, file), format, quality=quality)
                else:
                    img.save(os.path.join(args.output_dir, file), format, quality=quality)

            # Try clean this up a little with a list of extensions
            file_extensions = ['.txt', '.caption', '.tags', '.exiftxt']
            # Loop each extension
            for ext in file_extensions:
                file_to_copy = base_file + ext

                if args.keep_relative:
                    output_path = os.path.join(args.output_dir, rel_path)
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    file_src = os.path.join(root, file_to_copy)
                    file_dst = os.path.join(output_path, file_to_copy)
                else:
                    file_src = os.path.join(root, file_to_copy)
                    file_dst = os.path.join(args.output_dir, file_to_copy)

                # Check if the file with the current extension exists and copy if it does
                if os.path.exists(file_src):
                    # If it exists, copy it
                    shutil.copy2(file_src, file_dst)
                    # Let's keep those witty comments coming!
