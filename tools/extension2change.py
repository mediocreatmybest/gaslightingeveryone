import argparse
import os
import shutil

from func import walk_path


def change_file_ext(file_path, new_ext):
    new_path = os.path.splitext(file_path)[0] + new_ext
    shutil.move(file_path, new_path)


def process_files(input_directory, original_ext, new_ext, recursive_level='full'):
    # Use walk_path for filtered files
    if original_ext:
        files_to_change = walk_path(input_directory, [original_ext], recursive_level)
    # Set this up for later to support all files
    # call our file extension change func
    for file_path in files_to_change:
        change_file_ext(file_path, new_ext)


def main():
    parser = argparse.ArgumentParser(description='Change file extensions in bulk')
    parser.add_argument('--input', type=str, help='Input directory', metavar='/folder/ or c:\\folder', required=True)
    parser.add_argument('--ext', type=str, help='File extension to change', metavar='.tags', required=True)
    parser.add_argument('--new-ext', type=str, help='New file extension', metavar=".txt", required=True)
    parser.add_argument('--disable-recursive', action='store_true', help='Disable recursive search')

    args = parser.parse_args()
    # Disable recursive os walk if flagged, need this clean these functions up, feel free! Please...
    if args.disable_recursive:
        recursive_level = 1
    else:
        recursive_level = 'full'

    process_files(args.input, args.ext, args.new_ext, recursive_level)


if __name__ == '__main__':
    main()