import math
import warnings
from typing import List, Tuple

from PIL import Image


def ar_xy_to_float(xy):
    """Aspect ratio in X:Y to a float

    Args:
        xy ('1:1, 3:4, 16:9'): returns a list of floats from X:Y string

    Returns:
        float: returns the aspect ratio as a tuple of floats
    """
    ratios = xy.split(',')
    ratios = [tuple(map(float, r.split(':'))) for r in ratios]
    return [x/y for x, y in ratios]


def crop_to_set_aspect_ratio(image, aspect_ratios: List[float], debug=False) -> Tuple:
    """
    Crop an image to the closest allowed aspect ratio.

    image: the input image to be cropped
    aspect_ratios: a list of allowed aspect ratios as float values
    Returns:
        The cropped image
    """

    # Copy image instead of using original, not sure I need to do this
    img = image.copy()
    # Simple width by height from image size
    width, height = img.size
    # Devide width by height for ratio
    original_ratio = width / height

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

    # Would closest_ratio == original_ratio be better? Not sure
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
        print('Width x Height: ', width, 'x', height)
        print('Original aspect ratio: ', original_ratio)
        print('Allowed aspect ratios: ', aspect_ratios)
        print('Closest aspect ratio: ', closest_ratio)
        print('Distance from closest ratio: ', closest_distance)

    return img


def pad_to_1_to_1(image):
    """Does a simple pad to 1:1 aspect ratio

    Args:
        image: Pass in an image object

    Returns:
        image: returns the image object padded 1:1
    """
    width, height = image.size
    # Use max to return the largest side
    max_side = max(width, height)
    # Create new image with black background with max_side on both sides
    new_img = Image.new("RGB", (max_side, max_side), (0, 0, 0))
    # Paste image into new image, No other calculations. phew.
    new_img.paste(image, (int((max_side - width) / 2), int((max_side - height) / 2)))
    return new_img


def crop_to_multiple(image, multiple=64):
    """
    Crop an image to a multiple of a given number in pixels (64 by default).

    Parameters:
        image (PIL.Image): The image to be cropped.
        multiple (int, optional): The multiple to which the image should be cropped. Defaults to 64.

    Returns:
        PIL.Image: The cropped image.
    """
    width, height = image.size
    new_width = (width // multiple) * multiple
    new_height = (height // multiple) * multiple
    left = int((width - new_width) / 2)
    upper = int((height - new_height) / 2)
    return image.crop((left, upper, left + new_width, upper + new_height))


def resize_side_size(image, min_size, resize_mode='smallest'):
    """
    Resize an image to a specific size based on the smallest side of the image.

    Parameters:
        image (PIL.Image): The image to be resized.
        min_size (int): The size to which the smallest side of the image should be resized.

    Returns:
        PIL.Image: The resized image.

    Raises:
        warnings.warn: If `min_size` is equal or larger than the smallest side of the source image.
    """
    # Get width and height frm the PIL image.size
    width, height = image.size

    if resize_mode == 'smallest':
        # Resize based on the smallest side of the PIL image
        if min_size >= min(width, height):
            warnings.warn(f'Beep boop! The size you specified: {min_size} is equal or larger than the source image: {image.size}, enlarging instead.', stacklevel=2)
        if width < height:
            new_size = (min_size, int(height * min_size / width))
        else:
            new_size = (int(width * min_size / height), min_size)

    elif resize_mode == 'largest':
        # Resize based on the largest side of the PIL image
        if min_size >= max(width, height):
            warnings.warn(f'Beep boop! The size you specified: {min_size} is equal or larger than the source image: {image.size}, enlarging instead.', stacklevel=2)
        if width < height:
            new_size = (int(width * min_size / height), min_size)
        else:
            new_size = (min_size, int(height * min_size / width))
    else:
        raise ValueError('Beep!, please use "smallest" or "largest')

    # return the resized PIL image
    return image.resize(new_size)

if __name__ == '__main__':
    print('\n')
    print('This function contains the following: ')
    print('\n')
    print('Aspect Crop Function')
    print('for example: ')
    print('image = crop_to_set_aspect_ratio(image, aspect_ratios)')
    print('\n')
    print('Crop to Multiple Function')
    print('for example: ')
    print('image = crop_to_multiple(image, multiple)')
    print('or: ')
    print('image = crop_to_multiple(image_object, 64)')
    print('\n')
    print ('resize on side size Function)')
    print('for example: ')
    print('image = resize_side_size(image, min_size)')
    print('or: ')
    print('image = resize_side_size(image_object, 1024)')
    print('\n')
    print ('Simple Pad Image Function)')
    print('for example: ')
    print('image = pad_to_1_to_1(image_object)')
    print('\n')
    print('from multi_crop_func import *')
    print('\n')

