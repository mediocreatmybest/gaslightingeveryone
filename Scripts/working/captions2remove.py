import os
import re
import argparse
import platform

from pathlib import Path
from tqdm import tqdm

# Create the arg parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--captiondir', type=str, help='Directory with captions', metavar='c:\images', required=True)
parser.add_argument('--caption-remove', type=str, help='Text to remove', metavar='"Monkey Magic is great!', required=True)
parser.add_argument('--caption-replace', type=str, help='Image directory to caption', metavar='"Tripitaka is the best!"', required=True)
parser.add_argument('--extension', type=str, help='File extension of caption files e.g. ".txt"', metavar='".txt"', default='.txt', required=False)
# Debug 
parser.add_argument('--debug', action='store_true', help='Disables Saving files, prints output locations', required=False)

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
                print('######################################')

            # Open the found caption file ending with .txt (TODO: update to allow string re.sub on any extension)
            with open(caption_file, 'r', encoding='UTF-8') as caption_read:
                data = caption_read.read()
                # Push argument into new variable and run re.sub to remove specified text 
                replacement_str = re.sub(rf'{cmd_args.caption_remove}', rf'{cmd_args.caption_replace}', data, flags=re.I)
                if cmd_args.debug is True:
                    print('Data in txt file before re.sub: ')
                    print('######################################')
                    print(data)
                    print('######################################')
                    print('String to find: ', cmd_args.caption_remove)
                    print('String to insert: ', cmd_args.caption_replace)
                    print('Complete string is now: ')
                    print('######################################')
                    print(replacement_str)
                    print('######################################')

            # Quick fix to work if platform.system() == "Windows", maybe switch to path?
            if platform.system() == "Windows":
                pathsep = "\\"
            else:
                pathsep = "/"
            
            # Check if debug is enabled to disable saving
            if cmd_args.debug is True:
                savefiles = False
            else:
                savefiles = True

            # Set write flag to overwrite 
            writeflag = 'w'

            if cmd_args.debug is True:
                print('Set to overwrite existing files', writeflag)

            # Create new file and overwrite if exists
            if savefiles is True:
                with open(caption_file, f'{writeflag}', encoding='UTF-8') as f:
                    f.write(replacement_str)
                    f.close