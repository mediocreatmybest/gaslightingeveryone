import os
import argparse
import cv2
import shutil
from PIL import Image

# Create the parser
parser = argparse.ArgumentParser(description='Copy and resize all images in a directory recursively based on the shortest side while keeping the same name')

# Set allowed images for directory scan (Sorry GIF)
image_filter = ('jpeg','jpg','png','bmp','webp')

# Add the arguments
parser.add_argument('--input-dir', metavar='c:\images', type=str,
 help='the input image directory path', required=True)
parser.add_argument('--output-dir', metavar='c:\images_resize', type=str,
 help='the image output directory path', required=True)
parser.add_argument('--keep-relative', action='store_true', default=True,
 help='Keep relative folder structure with output directory, on by default')
parser.add_argument('--size', metavar='576', type=int,
 help='desired size of the smallest side', required=True)
parser.add_argument('--copy-format', action='store_true', default=False,
 help='Keeps the same file format from the input image')
parser.add_argument('--format', metavar='jpg', type=str,
 help=f'Change the image format {image_filter}')
parser.add_argument('--crop', action='store_true', default=False,
 help='Enable image cropping to closest aspect ratio')
parser.add_argument("--aspect_ratios", type=str, default="4:3,3:4,16:9,9:16,1:1",
 help="Comma-separated list of allowed aspect ratios, only used with crop argument")

# Parse the arguments
args = parser.parse_args()
# Set aspect ratio for cropping later
aspect_ratios = args.aspect_ratios.split(",")

# Create error if copy-format is False and the format argument is None
if args.copy_format is False and args.format is None:
    raise Exception('Please select a format, use one of the following: --format or --format-copy')

# Lets create the output directory if it doesn't exist
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)


def crop_image(image_path, aspect_ratios, min_size):
    """ Crop image to closest aspect ratio and resize to meet size argument """
    # Load the image
    image = cv2.imread(image_path)

    # Get the image aspect ratio
    h, w = image.shape[:2]
    image_ar = w / h

    # Convert aspect ratio inputs to floats
    aspect_ratios = [float(ar.replace(':', '.')) for ar in aspect_ratios]

    # Find closest aspect ratio
    closest_ar = min(aspect_ratios, key=lambda x: abs(x - image_ar))

    # Crop image to closest aspect ratio
    if closest_ar > image_ar:
        new_w = int(closest_ar * h)
        new_image = image[:, (w-new_w)//2:(w-new_w)//2+new_w]
    else:
        new_h = int(w / closest_ar)
        new_image = image[(h-new_h)//2:(h-new_h)//2+new_h, :]

    # Resize image to meet minimum size requirement as per size argument
    new_h, new_w = new_image.shape[:2]
    if min(new_h, new_w) < min_size:
        scale = min_size / min(new_h, new_w)
        new_image = cv2.resize(new_image, None, fx=scale, fy=scale)

    # Save and return the cropped image (I think this works)
    cv2.imwrite(image_path, new_image)
    return new_image

def resize_image(file, args, image_filter):
    """ Resize image based on smallest side and
     attempting to move this into its own function """
    # Apply basic image filter (Sorry GIF) we also want to be insensitive like Jann Arden
    if file.casefold().endswith(image_filter):
        # Open the image
        image = Image.open(file)

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
    return resized_image


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