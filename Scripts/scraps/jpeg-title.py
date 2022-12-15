#!/usr/bin/env python
#https://code.adonline.id.au/reading-exif-data-in-python/

import imageio.v2 as imageio
import exifread
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from PIL.PngImagePlugin import PngImageFile, PngInfo
import re
import os
from rawphoto.cr2 import Cr2
from rawphoto.nef import Nef
import argparse


def options():
    parser = argparse.ArgumentParser(description="Read image metadata")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    args = parser.parse_args()
    return args

# Via https://gist.github.com/SamWhited/af58edaed66414bded84
def raw_metadata(raw, ifd, level=1):
    for name in ifd.entries:
        e = ifd.entries[name]
        if name in ifd.subifds or isinstance(name, tuple):
            if isinstance(name, tuple):
                for n in name:
                    print(level * "\t" + n + ":")
                    raw_metadata(raw, ifd.subifds[n], level + 1)
            else:
                print(level * "\t" + name + ":")
                raw_metadata(raw, ifd.subifds[name], level + 1)
        else:
            if isinstance(name, str):
                if e.tag_type_key == 0x07:
                    print(level * "\t" + "{}: {}".format(
                        name,
                        "[Binary blob]"
                    ))
                else:
                    print(level * "\t" + "{}: {}".format(
                        name,
                        ifd.get_value(e)
                    ))

def gen_metadata(image):

    # Read image into imageio for data type
    pic = imageio.imread(image)

    # Read image into PIL to extract basic metadata
    type = Image.open(image)

    # Calculations
    megapixels = (type.size[0]*type.size[1]/1000000) # Megapixels
    d = re.sub(r'[a-z]', '', str(pic.dtype)) # Dtype
    t = len(Image.Image.getbands(type)) # Number of channels

    print("\n--Summary--\n")
    print("Filename: ",type.filename)
    print("Format: ", type.format)
    print("Data Type:", pic.dtype)
    print("Bit Depth (per Channel):", d)
    print("Bit Depth (per Pixel): ", int(d)*int(t))
    print("Number of Channels: ", t)
    print("Mode: ",type.mode)
    print("Palette: ",type.palette)
    print("Width: ", type.size[0])
    print("Height: ", type.size[1])
    print("Megapixels: ",megapixels)

    # Open image with ExifMode to collect EXIF data
    exif_tags = open(image, 'rb')
    tags = exifread.process_file(exif_tags)

    # Create an empty array
    exif_array = []

    # Print header
    print("\n--Metadata--\n")

    # For non-PNGs
    if type.format != "PNG":
        # Compile array from tags dict
        for i in tags:
            compile = i, str(tags[i])
            exif_array.append(compile)
        for properties in exif_array:
            if properties[0] != 'JPEGThumbnail':
                print(': '.join(str(x) for x in properties))

    if type.format == "PNG":
        image = PngImageFile(image) #via https://stackoverflow.com/a/58399815
        metadata = PngInfo()

        # Compile array from tags dict
        for i in image.text:
            compile = i, str(image.text[i])
            exif_array.append(compile)

        # If XML metadata, pull out data by idenifying data type and gathering useful meta
        if len(exif_array) > 0:
                header = exif_array[0][0]
        else:
            header = ""
            print("No available metadata")

        xml_output = []
        if header.startswith("XML"):
            xml = exif_array[0][1]
            xml_output.extend(xml.splitlines()) # Use splitlines so that you have a list containing each line
            # Remove useless meta tags
            for line in xml.splitlines():
                if "<" not in line:
                    if "xmlns" not in line:
                        # Remove equal signs, quotation marks, /> characters and leading spaces
                        xml_line = re.sub(r'[a-z]*:', '', line).replace('="', ': ')
                        xml_line = xml_line.rstrip(' />')
                        xml_line = xml_line.rstrip('\"')
                        xml_line = xml_line.lstrip(' ')
                        print(xml_line)

        elif header.startswith("Software"):
            print("No available metadata")

        # If no XML, print available metadata
        else:
            for properties in exif_array:
                if properties[0] != 'JPEGThumbnail':
                    print(': '.join(str(x) for x in properties))


    # Explanation for GIF or BMP
    if type.format == "GIF" or type.format == "BMP":
        print("No available metadata")

def main():

    # Get options
    args = options()
    image = args.image

    # Check for RAW images

    name, extension = os.path.splitext(image)

    # List valid extensions
    ext = [".png", ".jpg", ".jpeg", ".cr2", ".nef", ".tif", ".bmp"]
    if extension not in ext:
        print("File format ",extension," not supported.")
        exit()

    if extension == ".CR2":
        metadata = {}
        filepath = image
        (filepath_no_ext, ext) = os.path.splitext(filepath)
        filename_no_ext = os.path.basename(filepath_no_ext)
        ext = ext.upper()
        if ext == '.CR2':
            raw = Cr2(filename=filepath)
        elif ext == '.NEF':
            raw = Nef(filename=filepath)
        else:
            raise TypeError("Format not supported")
        for i in range(len(raw.ifds)):
            ifd = raw.ifds[i]
            print("IFD #{}".format(i))
            raw_metadata(raw, ifd)
            # Hax.
            for subifd in ifd.subifds:
                if isinstance(subifd, int):
                    print("Subifd ", subifd)
                    raw_metadata(raw, ifd.subifds[subifd], 1)
        raw.close()

    else:
        gen_metadata(image)




if __name__ == '__main__':
    main()