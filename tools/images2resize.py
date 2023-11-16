import argparse
import configparser
import os
import shutil

from PIL import Image
from PIL.Image import Resampling

# Sort imports is super handy! Thanks VS Code!
from func_image import (check_trans_background, crop_to_multiple,
                        crop_to_set_aspect_ratio, pad_to_1_to_1,
                        replace_trans_background, resize_side_size)
# Time to test OS Walk Plus function to add file filtering and depth control.
# I'm totally sure this doesn't have any bugs and works on every OS.
from func_os_walk_plus import os_walk_plus

# Create the parser --> I think I should create a config version to make this a little easier.
parser = argparse.ArgumentParser(description='Copy, crop, and resize all images in a directory recursively')

# Set allowed images for directory scan (Sorry GIF)
image_filter = ('jpeg','jpg','png','bmp','webp')

# Set our dictionary mapping with resampling method names for PIL
# Switch to resampling module due to DeprecationWarning for Image.xyz
resampling_methods = {
    'antialias': Resampling.LANCZOS,  # ANTIALIAS is LANCZOS
    'nearest': Resampling.NEAREST,
    'box': Resampling.BOX,
    'bilinear': Resampling.BILINEAR,
    'hamming': Resampling.HAMMING,
    'bicubic': Resampling.BICUBIC,
    'lanczos': Resampling.LANCZOS
}

def read_config_file(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def debug_print(variables, debug_mode):
    if debug_mode:
        # Start of loop
        print('############ Start Loop ############ -->')
        for variable_name, variable_value in variables.items():
            if variable_name == 'keep_relative':
                print(f'keep_relative: {variable_value}')
            elif variable_name == 'file':
                print(f'file: {variable_value}')
            elif variable_name == 'multiples_crop':
                print(f'multiples_crop: {variable_value}')
            elif variable_name == 'aspect_crop':
                print(f'aspect_crop: {variable_value}')
            elif variable_name == 'resize':
                print(f'resize: {variable_value}')
            elif variable_name == 'resize_mode':
                print(f'resize_mode: {variable_value}')
            elif variable_name == 'image':
                print(f'Original image size: {variable_name}.size: {variable_value.size}')
            elif variable_name == 'img':
                print(f'New image size: {variable_name}.size: {variable_value.size}')
            elif variable_name == 'min_size':
                print(f'min_size: {variable_value}')
        # End of loop
        print('<-- ############ End Loop ############\n')

# Add the arguments
parser.add_argument('--input-dir', metavar='c:\images', type=str,
                    help='the input image directory path', required=False)
parser.add_argument('--output-dir', metavar='c:\images_resize', type=str,
                    help='the image output directory path', required=False)
parser.add_argument('--disable-keep-relative', action='store_false', default=None,
                    help='Disables the relative folder structure with output directory, this will output into a single folder')
parser.add_argument('--format', metavar='jpg', type=str,
                    help=f'Change the image format {image_filter} or use "copy" to keep the current format')
parser.add_argument('--multiples-crop', action='store_true', default=False,
                    help='Crops the image to the closest specified multiple')
parser.add_argument('--multiples-of', metavar='64', default=64, type=int,
                    help='Desired image size in multiples of pixel count e.g 64', required=False)
parser.add_argument('--aspect-crop', action='store_true', default=False,
                    help='Crops the image to the closest aspect ratio')
parser.add_argument('--aspect-ratios', type=str,
                    help='Set desired aspect ratios as a float in comma seperated list e.g 0.56,0.75,0.8,1,1.33,1.5,1.6,1.78')
parser.add_argument('--resize', action='store_true', default=False,
                    help='Flags to resize to the specified min_size while maintaining current or set aspect ratio')
parser.add_argument('--resize-mode', type=str,
                    help='Resize modes: smallest (resizes based on smallest side of image), largest (resizes on largest side of image)',
                    choices=['smallest', 'largest'], required=False)
parser.add_argument('--resample-mode', type=str,  default='antialias',
                    help='Resize modes: smallest (resizes based on short side of image), largest (resizes on long side of image)',
                    choices=resampling_methods.keys(), required=False)
parser.add_argument('--min-size', metavar='768', type=int,
                    help='desired size of the smallest side', required=False)
parser.add_argument('--skip-smaller', action='store_true',
                    help='Skips resizing images that are smaller than the minimum size, this avoids enlarging images')
parser.add_argument('--pad-image', action='store_true', default=False,
                    help='Pads the image to a 1:1 ratio')
parser.add_argument('--color', type=str,
                    help='Manually specify a colour for transparent background replacement in format: R,G,B')
parser.add_argument('--common-colors", action="store_true',
                    help='Use a limited number of simple background colours for transparent ground replacement')
parser.add_argument('--config', '-c', metavar='config.ini', type=str,
                    help='Use a config file to set options')
parser.add_argument('--debug', action='store_true', default=False,
                    help='Print debug messages of output images', required=False)

# Parse the arguments
args = parser.parse_args()

# Lets check if a config file is being used, less clutter for the cli
if args.config:
    config = read_config_file(args.config)
else:
    # Add fallback configparser with config otherwise config fails if args.config isn't set
    config = configparser.ConfigParser()

# Set resampling method from dictionary
set_resampling_method = resampling_methods[args.resample_mode]

########################
# ConfigParse Settings #
########################
# Set bool defaults for fallback
fallback_true = True
fallback_false = False

# Input/Output section
input_dir = args.input_dir if args.input_dir else config.get('config', 'input_dir', fallback=None)
output_dir = args.output_dir if args.output_dir else config.get('config', 'output_dir', fallback=None)
# We need an input directory and and output, stop if None
if input_dir is None or output_dir is None:
    raise Exception('input directory or output directory missing! BEEP BOOP! Stopping!')
# Check if we are going to blitz out input directory. Let's not.
if input_dir and output_dir and os.path.abspath(input_dir) == os.path.abspath(output_dir):
    raise Exception("Input and output directory are the same. Please set a different output directory.")

# Set keep_relative to True if config or arg isn't present
keep_relative = args.disable_keep_relative if args.disable_keep_relative is not None else config.getboolean('config', 'keep_relative', fallback=fallback_true)

# Set format from args or config, default to 'copy'
output_format = args.format if args.format else config.get('config', 'format', fallback=None)

# Do you want to crop in miltiples?! Well, now you can! Exciting.
multiples_crop = args.multiples_crop if args.multiples_crop is not False else config.getboolean('config', 'multiples_crop', fallback=fallback_false)

# Get multiples_of pixels for cropping
multiples_of = args.multiples_of if args.multiples_crop else config.getint('config', 'multiples_of', fallback=8)

# Aspect ratio cropping, the most exciting feature! Well, not really... Maybe you need to crop something?!
# If I could offer you only one tip for the future, Aspect ratio cropping would be, "it".
# The long-term benefits of Aspect ratio cropping have been proven by scientists,
# whereas the rest of my advice has no basis more reliable than my own meandering experience. I will dispense this advice now.
aspect_crop = args.aspect_crop if args.aspect_crop is not False else config.getboolean('config', 'aspect_crop', fallback=fallback_false)

# Enjoy the power and beauty of your aspect ratios. Oh, never mind.
# You will not understand the power and beauty of your aspect ratios until they've faded... Ahem.
# Aspect ratios as a floating points or X:Y
ar_fallback = '1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 16:9, 9:16'
aspect_ratios_str = args.aspect_ratios if args.aspect_ratios else config.get('config', 'aspect_ratios', fallback=ar_fallback)

# Flag to resize images based on its small or largest side
resize = args.resize if args.resize is not False else config.getboolean('config', 'resize', fallback=fallback_false)

# Set which side to resize on, long or short, largest or smallest etc.
resize_mode = args.resize_mode if args.resize_mode else config.get('config', 'resize_mode', fallback='smallest')

# Set resample mode, Resample modes: antialias, nearest, box, bilinear, hamming, bicubic, lanczos
resample_mode = args.resample_mode if args.resample_mode else config.get('config', 'resample_mode', fallback='antialias')

# The minimum size in pixels for the smallest or largest side based on the selected resize mode.
min_size = args.min_size if args.min_size else config.getint('config', 'min_size', fallback=1280)

# Skips resizing images that are smaller than the minimum size (min_size). This avoids enlarging images
skip_smaller = args.skip_smaller if args.skip_smaller is not False else config.getboolean('config', 'skip_smaller', fallback=fallback_false)

# Pads the image to a 1:1 ratio, will either create Pillarboxes or Letterboxing
pad_image = args.pad_image if args.pad_image is not False else config.getboolean('config', 'pad_image', fallback=fallback_false)

# Manually specify a color for transparent background replacement (format: R, G, B)
color = args.color if args.color else config.get('config', 'color', fallback='211, 211, 211')

# Use a limited number of simple background colors for transparent ground replacement
common_colors = args.common_colors if args.common_colors is not False else config.getboolean('config', 'common_colors', fallback=fallback_false)

# Print debug messages of output images (Need to fix this up)
debug  = args.debug if args.debug is not False else config.getboolean('config', 'debug', fallback=fallback_false)

# End of config setup. Thank jebus.

# Convert the string or X:Y to a list of floats
aspect_ratios = aspect_ratios_str.split(',')
aspect_ratios = [float(r.split(':')[0]) / float(r.split(':')[1]) if ':' in r else float(r) for r in aspect_ratios]

# Lets create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Quick jog through all files in the input directory recursively, look at adding depth
for root, dirs, files in os_walk_plus(input_dir):
#for root, dirs, files in os.walk(input_dir):
    for file in files:
        # Find the base name for all files
        base_file = (os.path.splitext(file)[0])
        # Find relative path of the input directory and file
        rel_path = os.path.relpath(root, input_dir)
        # Apply basic image filter (Sorry GIF) we also want to be insensitive like Jann Arden
        if file.casefold().endswith(image_filter):
            # Open the image to get format
            image = Image.open(os.path.join(root, file))
            # Create a copy if we don't actually want to crop or resize *note to self* img.format is lost with a copy
            img = image.copy()

            # Set full path for functions
            #fullpath = os.path.join(root, file)

            if debug is True:
                debug_print(locals(), debug_mode=debug)

            # Set join_crop if aspect_crop and multiples_crop are being called together
            joint_crop = multiples_crop and aspect_crop
            # Use the resize_side_size function from multi_crop_func.py
            # This should be done before any other of my silly resizing functions

            # Do a joint crop if joint_crop is True - Keep this in the same function
            if joint_crop:
                img = crop_to_set_aspect_ratio(img, aspect_ratios, multiples=multiples_of, debug=debug)
                if debug is True:
                    debug_print(locals(), debug_mode=debug)
            else:
                if multiples_crop and not joint_crop:
                    img = crop_to_multiple(img, multiples_of)
                    if debug is True:
                        debug_print(locals(), debug_mode=debug)

                if aspect_crop and not joint_crop:
                    img = crop_to_set_aspect_ratio(img, aspect_ratios)
                    if debug is True:
                        debug_print(locals(), debug_mode=debug)

            if resize is True:
            # Moving resize to the end of the chain, so if we request 768, we *should* get 768
                img = resize_side_size(img, min_size=min_size,
                                        resize_mode=resize_mode,
                                        resample=set_resampling_method,
                                        skip_smaller=skip_smaller)
                if debug is True:
                    debug_print(locals(), debug_mode=debug)

            # Use the crop_to_multiple function from multi_crop_func.py
            # As we need to strip the image of these pixels first to maintain a useful image
            # This function should probably be done on its own
            #if multiples_crop is True:
            #    if resize is True:
            #        img = crop_to_multiple(img, multiples_of)
            #        if debug is True:
            #            debug_print(locals(), debug_mode=debug)
            #    else:
            #        img = crop_to_multiple(image, multiples_of)
            #        if debug is True:
            #            debug_print(locals(), debug_mode=debug)

            # Use the crop_to_aspect function from multi_crop_func.py
            # As we need to maintain x:y aspect ratio to keep multiples of arguments
            #if aspect_crop is True:
            #    if multiples_crop is True or resize is True:
            #        img = crop_to_set_aspect_ratio(img, aspect_ratios, debug=debug)
            #        if debug is True:
            #            debug_print(locals(), debug_mode=debug)
            #    else:
            #        img = crop_to_set_aspect_ratio(image, aspect_ratios, debug=debug)
            #        if debug is True:
            #            debug_print(locals(), debug_mode=debug)

            # Use Pad function from multi_crop_func.py
            # Basic padding to move an image to a 1:1 aspect ratio
            # Need to add debug
            if pad_image is True:
                if resize is True:
                    img = pad_to_1_to_1(img)
                else:
                    img = pad_to_1_to_1(image)

            # Add some options to check and remove alpha or transparent backgrounds with PIL
            # If replace transparent background with common colors is selected, replace with basic 9 colours
            if common_colors is True:
                if check_trans_background(img) is True:
                    img = replace_trans_background(img, common_colors=common_colors)
            # If common_colors and color is set, common colors runs first and therefor wins the chicken dinner
            if color:
                specified_color = tuple(map(int, color.split(",")))
                if check_trans_background(img) is True:
                    img = replace_trans_background(img, specified_color=specified_color)

            # Check for copy input format (I think this works) maybe, check for None as well.
            # Looks like only the original instance of image retains format the copy does not.
            output_format = image.format if output_format == 'copy' or output_format is None else output_format
            # Casefold it after PIL reports back format while yelling at me.
            output_format = output_format.casefold()

            # Set default quality for jpg and webp (95)
            quality = 95

            # PNG Compression level, add to config later
            compress_level = 6

            # Need to make this easier to read, so lets break it up.
            if keep_relative:
                output_path = os.path.join(output_dir, rel_path)
            else:
                output_path = output_dir
            # Create the folders if they don't exist
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Save the resized image recursively while checking for jpeg vs jpg with its silly extension arguments
            if output_format  == 'jpg':
                img.save(os.path.join(output_path, base_file + '.jpg'), 'jpeg', quality=quality)
            elif not output_format  == 'copy':
                img.save(os.path.join(output_path, base_file + '.' + output_format), output_format, quality=quality, compress_level=compress_level)
            # Back to copy existing format
            if output_format  == 'copy':
                img.save(os.path.join(output_path, file), output_format, quality=quality, compress_level=compress_level)

            # Try clean this up a little with a list of extensions
            file_extensions = ['.txt', '.caption', '.tags', '.exiftxt']
            # Loop each extension
            for ext in file_extensions:
                file_to_copy = base_file + ext
                file_src = os.path.join(root, file_to_copy)
                file_dst = os.path.join(output_path, file_to_copy)
                # Check if the file with the current extension exists and copy if it does
                if os.path.exists(file_src):
                    # If it exists, copy it
                    shutil.copy2(file_src, file_dst)