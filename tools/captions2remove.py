import os
import re
import argparse

from pathlib import Path
from tqdm import tqdm

# Save function

def save_file(file_path, data, mode='w', encoding='utf-8', debug=False):
    """ Function to save a file, defaults to write mode """
    if not debug:
        with open(file_path, mode, encoding=encoding) as f:
            f.write(data)
        print(f'File saved to {file_path}')
    else:
        print('Debug mode, file not saved')


def save_file_prepend(file_path, data, mode='r+', encoding='utf-8', debug=False):
    """ Function to save with 'r+' at the start of a file seek(0) """
    if not debug:
        with open(file_path, mode, encoding=encoding) as f:
            f.seek(0)
            f.write(data)
        print(f'File saved to {file_path}')
    else:
        print('Debug mode, file not saved')


# Create the arg parser
parser = argparse.ArgumentParser(description='Allows you to selection root folders and recursivly modify plain text files')
# Add an argument
parser.add_argument('--captiondir', type=str, help='Directory with captions', metavar='c:\images', required=True)
parser.add_argument('--caption-find', type=str, help='Text to find and remove', metavar='"Monkey Magic is great!"', required=False)
parser.add_argument('--caption-replace', type=str, help='Caption to change', metavar='"Tripitaka is the best!"', required=False)
parser.add_argument('--caption-prepend', type=str, help='Insert text at the start of the caption', metavar='"Wow text at the start? say it aint so!"', required=False)
parser.add_argument('--caption-append', type=str, help='Insert text at the end of the caption', metavar='"Wow text at the end? Amazing!"', required=False)
parser.add_argument('--extension', type=str, help='File extension of caption files e.g. ".txt"', metavar='".txt"', default='.txt', required=False)
# Debug
parser.add_argument('--debug', action='store_true', default=False, help='Disables Saving files, prints output locations', required=False)

# Parse the argument
cmd_args = parser.parse_args()

# Path to caption files.
captions_path = Path(rf"{cmd_args.captiondir}")

for root, dirs, files in os.walk(captions_path):
    for file in tqdm(files, desc="processing files", unit="regex2sub"):
        if file.endswith(f'{cmd_args.extension}'):
            caption_file = (os.path.join(root, file))
            caption_base_dir = (os.path.join(root))

            # Debug
            if cmd_args.debug is True:
                print('######################################')
                print('caption file: ', caption_file)
                print('image caption base directory: ', caption_base_dir)
                if cmd_args.caption_find:
                    print(f'--caption-find argument: {cmd_args.caption_find}')
                    print(f'--caption-replace argument: {cmd_args.caption_replace}')
                if cmd_args.caption_prepend:
                    print(f'--caption-prepend argument: {cmd_args.caption_prepend}')
                if cmd_args.caption_append:
                    print(f'--caption-append argument: {cmd_args.caption_append}')
                print('######################################')

            # Open the found caption file with different arguments

            if cmd_args.caption_find:
                with open(caption_file, 'r', encoding='utf-8') as ff:
                    data = ff.read()
                    # If replacing strings we want to push the argument into new variable and run re.sub to remove specified text
                    # Make omitting replace argument pass '' instead of None, this should allow simple removal without replacement arg
                    if cmd_args.caption_replace is None:
                        cmd_args.caption_replace = ''
                    replacement_data = re.sub(rf'{cmd_args.caption_find}', rf'{cmd_args.caption_replace}', data, flags=re.I)
                    save_file(file_path=caption_file, data=replacement_data, mode='w', debug=cmd_args.debug)

            if cmd_args.caption_prepend:
                # Time to save and move to the start of the file
                with open(caption_file, 'r', encoding='utf-8') as fp:
                    # Join the new data with the original data
                    data = fp.read()
                    prepend_data = cmd_args.caption_prepend + data
                    save_file_prepend(file_path=caption_file, data=prepend_data, mode='r+', debug=cmd_args.debug)

            if cmd_args.caption_append:
                    appended_data = cmd_args.caption_append
                    save_file(file_path=caption_file, data=appended_data, mode='a', debug=cmd_args.debug)