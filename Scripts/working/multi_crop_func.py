from PIL import Image

def aspect_crop_image(image_path, aspect_ratios):
    """ Crop an image to a given aspect ratio in the format W:H """
    # Parse allowed aspect ratios
    aspect_ratios = [float(x.split(':')[0])/float(x.split(':')[1]) for x in aspect_ratios.split(',')]

    # Open image
    img = Image.open(image_path)
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

def crop_to_multiple(image_path, multiple=64):
    """ Crop an image to a multiple of a given number in pixels (64 by default) """
    # Open image
    img = Image.open(image_path)
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

if __name__ == '__main__':
    print('Aspect Crop Function')

    print('Crop to Multiple Function')


