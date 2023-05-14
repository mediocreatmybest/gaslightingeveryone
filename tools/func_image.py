import math
import random
import warnings
from typing import List, Tuple

from PIL import Image
from PIL.Image import Resampling


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


def resize_side_size(image, min_size, resize_mode='smallest', resample=Resampling.LANCZOS, skip_smaller=False):
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
    # Get width and height from the PIL image.size
    width, height = image.size

    if skip_smaller and min(width, height) < min_size:
        warnings.warn(f'Skipping image as it is already smaller than the min_size: {min_size}', stacklevel=2)
        return image

    if resize_mode == 'smallest':
        # Resize based on the smallest side of the PIL image
        if min_size >= min(width, height):
            warnings.warn(
            f'Beep boop! The size you specified: {min_size} is equal or larger than '
            f'the source image: {image.size}, enlarging instead, use skip_smaller to skip',
            stacklevel=2)

        if width < height:
            new_size = (min_size, int(height * min_size / width))
        else:
            new_size = (int(width * min_size / height), min_size)

    elif resize_mode == 'largest':
        # Resize based on the largest side of the PIL image
        if min_size >= max(width, height):
            warnings.warn(
            f'Beep boop! The size you specified: {min_size} is equal or larger than '
            f'the source image: {image.size}, enlarging instead, use skip_smaller to skip',
            stacklevel=2)

        if width < height:
            new_size = (int(width * min_size / height), min_size)
        else:
            new_size = (min_size, int(height * min_size / width))
    else:
        raise ValueError('Beep!, please use "smallest" or "largest')

    # Set resample method, defaults to antialias
    resized_image = image.resize(new_size, resample=resample)
    # return the resized PIL image
    return resized_image



def random_color(common_colors=False):
    """
    Generates a random color in R, G, B. If common_colors is True, a random color from a list of common
    and neutral colors; otherwise, it returns a random color.

    args: common_colors (bool): use a list of common and neutral colors. Default is False.

    returns: A color tuple in R, G, B
    """
    if common_colors:
        common_color_list = [
            # A list of common and neutral colours, maybe we can get a better list, so far this will do.
            (255, 255, 255),  # White
            (242, 242, 242),  # Light Gray
            (245, 245, 245),  # White Smoke
            (224, 224, 224),  # Gainsboro
            (220, 220, 220),  # Silver
            (211, 211, 211),  # Light Steel Blue
            (192, 192, 192),  # Gray
            (176, 196, 222),  # Steel Blue
            (135, 206, 250),  # Light Sky Blue
            (240, 230, 140),  # Khaki
            (238, 232, 170),  # Pale Goldenrod
        ]
        # Roll the dice.
        return random.choice(common_color_list)
    else:
        # Unleash the rainbow! Some how it still kinda sucks, maybe we should look at gradients?
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def replace_trans_background(image, specified_color=None, common_colors=False):
    """
    Replaces a transparent background of a PIL image with a specified colour or a random color.

    args:   image (PIL.Image.Image): a PIL image.
            specified_color (tuple, optional): The colour for the transparent background with. Default is None.
            common_colors (bool, optional): Use a random colour from a list of common and neutral colours.
                                            This parameter is ignored if specified_color is provided. Default is False.

    Returns: PIL.Image.Image: the PIL image with the transparent background replaced.
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Input should be a PIL Image object")

    image = image.convert("RGBA")
    width, height = image.size

    if specified_color is None:
        # Let's get a background color that stands out, or not?
        background_color = random_color(common_colors)
    else:
        # Otherwise we do what the user wants, a specific colour. Pew Pew!
        background_color = specified_color

    # Create the new image with the selected background colour
    background = Image.new("RGBA", (width, height), background_color)
    # Paste paste paste! the original image onto the background
    background.paste(image, (0, 0), image)
    # Convert the image back to RGB mode (alpha channel shoo away)
    background = background.convert("RGB")

    return background

def check_trans_background(image):
    """
    Checks if an input image (in RGBA mode) has a transparent background.

    Args: image (PIL.Image.Image): The input PIL image in RGBA mode.

    Returns: bool: True if the image has a transparent background, or False maybe.
    """
    alpha_channel = image.split()[-1]
    # If the alpha channel is black and white or not completely opaque, then we have a transparent background, I think.
    # I'm sure this totally works as intended.
    return alpha_channel.mode == "1" or alpha_channel.getextrema() != (255, 255)

if __name__ == '__main__':
    print("Import Functions")