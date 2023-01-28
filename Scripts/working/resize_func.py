from PIL import Image

# Set set default allowed images for directory scan (Sorry GIF)
image_filter = ('jpeg','jpg','png','bmp','webp')

def resize_image(file, min_size, image_filter=image_filter):
    """ Resize image based on smallest side and
     attempting to move this into its own function """
    # Apply basic image filter (Sorry GIF) we also want to be insensitive like Jann Arden
    if file.casefold().endswith(image_filter):
        # Open the image
        image = Image.open(file)

        # Get the width and height of the image
        width, height = image.size
        if min_size >= min(width, height):
            # Better way to do this? It *should* still resize and keep toddling on
            try:
                raise ValueError((f'Beep boop! The size you specified: {min_size} is equal or larger than the source image: {file}'))
            except ValueError as err:
                print(err)

        # Determine the new size of the image
        if width < height:
            new_size = (min_size, int(height * min_size / width))
        else:
            new_size = (int(width * min_size / height), min_size)

        # Resize the image
        resized_image = image.resize(new_size)
    return resized_image

if __name__ == '__main__':
    print('Smallest Side Resizing Function')