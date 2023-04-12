import argparse
import os
import shutil

from func import walk_path
from sanitise_func import sanitise_char, sanitise_double_ext


def main(args):

    # Set depth for walk function in func.py
    if args.disable_recursive is True:
        depth = 1
    else:
        depth = 'full'
    # Set extension filtering, else None.
    if args.ext_filter:
        ext_filter = tuple(args.ext_filter)
    else:
        ext_filter = None

    # Set extension filter
    if ext_filter is None:
        result = walk_path(path=args.input, recursive_level=depth)
    else:
        result = walk_path(args.input, ext_filter, recursive_level=depth)

    # for the files in the results
    for file_path in result:
    # remove unwanted characters from the file name for windows and linux
        if args.sanitize_filename is True:
            new_filename = sanitise_char(os.path.basename(file_path), debug=False)
        else:
            new_filename = os.path.basename(file_path)

        # remove double file extensions if needed
        if args.remove_double_ext is True:
            new_filename = sanitise_double_ext(new_filename)

        # Set new file path
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)

        # Rename if needed
        if new_file_path != file_path:
            shutil.move(file_path, new_file_path)
            print(f"Renamed '{file_path}' to '{new_file_path}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A way to sanitizes filenames")

    parser.add_argument('--input', required=True, help="File path, so we know where to send the cleaner")
    parser.add_argument('--disable-recursive', action='store_true', help="Disable searching file path recursivly")
    parser.add_argument('--sanitize-filename', action='store_true', help="Sanitise filenames")
    parser.add_argument('--remove-double-ext', action='store_true', help="Remove double file extensions")
    parser.add_argument('--ext-filter', nargs='*', help="Extension filter")

    args = parser.parse_args()
    main(args)
