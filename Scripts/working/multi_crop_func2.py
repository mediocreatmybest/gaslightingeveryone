import math
from typing import List, Tuple

from PIL import Image


def crop_to_set_aspect_ratio(image, aspect_ratios: List[float], debug=False) -> Tuple:
    """
    Crop an image to the closest allowed aspect ratio.

    :param image: the input image to be cropped
    :param aspect_ratios: a list of allowed aspect ratios as float values
    :return: the cropped image
    """

    # Copy image instead of using original, not sure I need to do this
    img = image.copy()
    # Simple width by height from image size
    width, height = img.size
    # Devide width by height for ratio
    original_ratio = width / height

    # Convert the string to a list of floats ( Move to main script)
    aspect_ratios_split = [float(x) for x in aspect_ratios.split(',')]
    aspect_ratios = [x for x in aspect_ratios_split]

    closest_ratio = None
    closest_distance = math.inf
    for aspect_ratio in aspect_ratios:
        distance = abs(aspect_ratio - original_ratio)

        if distance < closest_distance:
            closest_ratio = aspect_ratio
            closest_distance = distance
            if closest_distance == 0:
                break

    if closest_ratio is None:
        raise ValueError(f"No valid aspect ratio was found among {aspect_ratios}")

    if math.isclose(closest_ratio, original_ratio):
        return img

    if closest_ratio > original_ratio:
        new_height = width / closest_ratio
        top = (height - new_height) / 2
        bottom = height - top
        img = img.crop((0, top, width, bottom))
    else:
        new_width = height * closest_ratio
        left = (width - new_width) / 2
        right = width - left
        img = img.crop((left, 0, right, height))

    if debug is True:
        print( 'Width x Height: ', width, 'x', height)
        print( 'Original aspect ratio: ', original_ratio)
        print('Allowed aspect ratios: ', aspect_ratios)
        print('Closest aspect ratio: ', closest_ratio)
        print('Distance from closest ratio: ', closest_distance)

    return img

def aspect_crop_float(image, aspect_ratios, debug=False):
    """ Crop an image to a given aspect ratio in a float e.g. 1.33 """
    # Parse allowed aspect ratios
    aspect_ratios = [x for x in aspect_ratios.split(',')]

    img = image.copy()
    width, height = img.size

    # Get original aspect ratio
    original_ratio = width / height

    # Find closest allowed aspect ratio
    closest_ratio = min([float(x) for x in aspect_ratios], key=lambda x: abs(x - original_ratio))

    # Crop image to closest allowed aspect ratio
    if closest_ratio > original_ratio:
        # Crop top and bottom
        new_height = width / closest_ratio
        top = (height - new_height) / 2
        bottom = height - top
        img = img.crop((0, top, width, bottom))
    else:
        # Crop left and right
        new_width = height * closest_ratio
        left = (width - new_width) / 2
        right = width - left
        img = img.crop((left, 0, right, height))

    # return image
    return img

def aspect_crop_float2(image, aspect_ratios, debug=False):
    """ Crop an image to a given aspect ratio in a float e.g. 1.33 """
    # Parse allowed aspect ratios
    aspect_ratios = [x for x in aspect_ratios.split(',')]

    img = image.copy()
    width, height = img.size

    # Get original aspect ratio
    original_ratio = width / height

    # Find closest allowed aspect ratio
    closest_ratio = min([float(x) for x in aspect_ratios], key=lambda x: abs(x - original_ratio))

    # Crop image to closest allowed aspect ratio
    if closest_ratio > original_ratio:
        # Crop top and bottom
        new_height = width / closest_ratio
        top = (height - new_height) / 2
        bottom = height - top
        img = img.crop((0, top, width, bottom))
    else:
        # Crop left and right
        new_width = height * closest_ratio
        left = (width - new_width) / 2
        right = width - left
        img = img.crop((left, 0, right, height))

    # Lets try this again, catch problem images
    width, height = img.size

    print('width is: ', width)
    print('height is: ', height)

    # Get original aspect ratio
    check_ratio = width / height

    # Find closest allowed aspect ratio
    check_closest_ratio = min([float(x) for x in aspect_ratios], key=lambda x: abs(x - check_ratio))

    print('closest ratio is: ', check_closest_ratio)
    print('check_ratio is: ', check_ratio)
    if check_closest_ratio == check_ratio:
        print('Nothing to do, RETURN')
        print('check_closest_ratio is: ', check_closest_ratio)
        print('check_ratio is: ', check_ratio)

        return img


    # Crop image to closest allowed aspect ratio
    if check_closest_ratio < check_ratio:
        # Crop top and bottom
        new_height = width / check_closest_ratio
        print('New Height:', new_height)
        top = (height - new_height) / 2
        bottom = height - top
        img = img.crop((0, top, width, bottom))
    else:
        # Crop left and right
        new_width = height * check_closest_ratio
        print('New width: ', new_width)
        left = (width - new_width) / 2
        right = width - left
        img = img.crop((left, 0, right, height))

    # return image
    return img

def crop_to_multiple(image, multiple=64):
    """ Crop an image to a multiple of a given number in pixels (64 by default) """

    img = image.copy()
    # Get the current width and height of the image
    width, height = img.size

    # Calculate the new width and height of the image
    new_width = (width // multiple) * multiple
    new_height = (height // multiple) * multiple

    # Calculate the left and upper coordinates of the crop box
    left = (width - new_width) / 2
    upper = (height - new_height) / 2

    # Crop the image
    img = img.crop((left, upper, left + new_width, upper + new_height))

    return img


def resize_small_side(image, min_size):
    """ Resize an image to a specific size based on the smallest side of the image """

    img = image.copy()

    # Get the width and height of the image
    width, height = img.size
    if min_size >= min(width, height):
        # Better way to do this? It *should* still resize and keep toddling on
        try:
            raise ValueError((f'Beep boop! The size you specified: {min_size} is equal or larger than the source image: {img.size}, enlarging instead.'))
        except ValueError as err:
            print(err)

    # Determine the new size of the image
    if width < height:
        new_size = (min_size, int(height * min_size / width))
    else:
        new_size = (int(width * min_size / height), min_size)

    # Resize the image
    img = img.resize(new_size)
    return img

if __name__ == '__main__':
    print('This script is designed to be imported into another script')
    print('It contains the following functions: ')
    print('\n')
    print('Aspect Crop Function')
    print('for example: ')
    print('image = aspect_crop_image(image, aspect_ratios)')
    print('or: ')
    print('image = aspect_crop_image(image_object, 1:1,4:3,16:9)')
    print('\n')
    print('Crop to Multiple Function')
    print('for example: ')
    print('image = crop_to_multiple(image, multiple)')
    print('or: ')
    print('image = crop_to_multiple(image_object, 64)')
    print('\n')
    print ('resize on small side Function)')
    print('for example: ')
    print('image = resize_small_side(image, min_size, image_filter)')
    print('or: ')
    print('image = resize_small_side(image_object, 1024)')
    print('\n')
    print('from multi_crop_func import *')
    print('\n')