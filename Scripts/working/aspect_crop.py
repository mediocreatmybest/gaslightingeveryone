import argparse
from PIL import Image

def aspect_crop_image(image_dir, aspect_ratios):
    # Parse allowed aspect ratios
    aspect_ratios = [float(x.split(':')[0])/float(x.split(':')[1]) for x in aspect_ratios.split(',')]

    # Open image
    img = Image.open(image_dir)
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-dir', required=True)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--aspect-ratios', required=True)
    args = parser.parse_args()

    image = aspect_crop_image(args.image_dir, args.aspect_ratios)

    image.save(args.output_dir)