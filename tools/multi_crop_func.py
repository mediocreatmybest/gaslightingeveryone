from PIL import Image

def aspect_crop(image, aspect_ratios):
    """ Crop an image to a given aspect ratio in the format W:H """
    # Parse allowed aspect ratios
    aspect_ratios = [float(x.split(':')[0])/float(x.split(':')[1]) for x in aspect_ratios.split(',')]

    img = image.copy()
    width, height = img.size

    # Get original aspect ratio
    original_ratio = width / height

    # Find closest allowed aspect ratio
    closest_ratio = min(aspect_ratios, key=lambda x: abs(x - original_ratio))

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

from PIL import Image

def aspect_crop_float(image, aspect_ratios):
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