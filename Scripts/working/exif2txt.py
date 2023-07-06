import argparse
import os
import exiftool
import pathlib

def extract_metadata(image_path):
    """
    Extract image metadata using exiftool binary and exiftool wrapper pyexiftool

    Args:
        image_path (Path): Path to image

    Returns:
        str: metadata
    """
    # TODO: add linux option and move to path
    with exiftool.ExifTool(executable="c:\\windows\\exiftool.exe") as et:
        metadata = et.execute_json("-G", "-n", "-u", "-j", str(image_path))[0]
    return metadata

def write_metadata_to_text_file(image_path):
    """
    write meta data to text file

    Args:
        image_path: path to image
    """
    metadata = extract_metadata(image_path)
    path = pathlib.Path(image_path)
    #TODO: add option to change output file extension
    text_path = path.with_suffix('.exiftxt')
    # Set dict names to do some word swapping
    # TODO: create word swap file
    tag_names = {'EXIF:Model': 'A photograph with',
                 'EXIF:FNumber': 'Aperture of',
                 'EXIF:ExposureTime': 'Shutter Speed',
                 'EXIF:ISO': 'ISO',
                 'EXIF:FocalLength': 'Focal Length',
                 'EXIF:LensModel': 'Lens'}
    values = []
    for tag, name in tag_names.items():
        value = metadata.get(tag)
        if value is not None and value != '':
            if tag == 'EXIF:ExposureTime':
                if value < 1:
                    value = f"1/{int(round(1/value)):.0f}"
                else:
                    value = f"{value:.0f}"
            elif tag == 'EXIF:FNumber':
                value = f"ƒ/{value:.1f}"
            elif tag == 'EXIF:FocalLength':
                value = f"{value:.0f}mm"
            values.append(f"{name} {value}")
    if len(values) > 0:
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(', '.join(values))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract EXIF metadata from image files with EXIF tool')
    parser.add_argument('--input', type=str, help='The root directory to search for image files.', required='true')
    args = parser.parse_args()

    # OS Walk with arguments for some default images
    # TODO: Switch to OS Walk Plus with file filters
    for root, dirs, files in os.walk(args.input):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                image_path = os.path.join(root, file)
                try:
                    write_metadata_to_text_file(image_path)
                    print(f"Metadata processed for {image_path}")
                except Exception as e:
                    print(f"Error writing metadata for {image_path}: {e}")