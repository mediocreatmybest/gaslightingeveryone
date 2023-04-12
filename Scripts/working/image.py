import Image
# From https://stackoverflow.com/questions/4744372/reducing-the-width-height-of-an-image-to-fit-a-given-aspect-ratio-how-python

image  = Image.open('images/original.jpg')
width  = image.size[0]
height = image.size[1]

aspect = width / float(height)

ideal_width = 200
ideal_height = 200

ideal_aspect = ideal_width / float(ideal_height)

if aspect > ideal_aspect:
    # Then crop the left and right edges:
    new_width = int(ideal_aspect * height)
    offset = (width - new_width) / 2
    resize = (offset, 0, width - offset, height)
else:
    # ... crop the top and bottom:
    new_height = int(width / ideal_aspect)
    offset = (height - new_height) / 2
    resize = (0, offset, width, height - offset)

thumb = image.crop(resize).resize((ideal_width, ideal_height), Image.ANTIALIAS)
thumb.save('thumb.jpg')