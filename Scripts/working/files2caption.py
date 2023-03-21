import argparse
import os

def create_caption(path, force=False, extension='txt', encoding='utf-8', debug=False):
    """
    Creates a new caption file for the specified file or directory of files if it doesn't exist.
    path: The path to the source file or directory.
    force: Force overwriting of existing caption files. Defaults to False.
    TODO:  debug, file filter
    add file filter in e.g if file.casefold().endswith(file_filter):
    """
    # If path is a directory, process all files in the directory
    if os.path.isdir(path):
        # Loop through each file in the directory
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            # Check if the file is a regular file
            if os.path.isfile(filepath):
                # Create a new filename with .txt extension
                new_filename = os.path.splitext(filename)[0] + '.' + extension
                new_filepath = os.path.join(path, new_filename)
                # Check if the new file already exists
                if os.path.exists(new_filepath):
                    # Force overwriting the existing file
                    if force:
                        print(f"Overwriting {new_filepath}")
                    else:
                        print(f"{new_filepath} already exists, skipping.")
                        continue
                # Open the original file and read its contents
                with open(filepath, 'r') as f:
                    # Create a new text file and write the contents of the original file to it
                    with open(new_filepath, 'w') as new_file:
                        new_file.write(f.read())

    # If path is a file, process the single file
    elif os.path.isfile(path):
        # Create a new filename with .txt extension
        new_filename = os.path.splitext(os.path.basename(path))[0] + '.txt'
        new_filepath = os.path.join(os.path.dirname(path), new_filename)
        # Check if the new file already exists
        if os.path.exists(new_filepath):
            # Force overwriting the existing file
            if force:
                print(f"Overwriting {new_filepath}")
            else:
                print(f"{new_filepath} already exists, skipping.")
                return
        # Open the original file and read its contents
        with open(path, 'r', encloding=encoding) as f:
            # Create a new text file and write the contents of the original file to it
            with open(new_filepath, 'w', encoding=encoding) as new_file:
                new_file.write(f.read())

    # If path does not exist, print an error message
    else:
        print(f"Error: {path} does not exist.")

def list_missing_captions(path, extension='txt', debug=False):
    """
    Lists all files that don't have a corresponding caption file.
    path: The path to the source file or directory.
    extension: sets manual extension e.g txt
    TODO: debug, filefilter
    add file filter in e.g if file.casefold().endswith(file_filter):
    """
    # If path is a directory, process all files in the directory
    if os.path.isdir(path):
        # Loop through each file in the directory
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            # Check if the file is a regular file
            if os.path.isfile(filepath):
                # Create a new filename with .txt extension
                new_filename = os.path.splitext(filename)[0] + '.' + extension
                new_filepath = os.path.join(path, new_filename)
                # Check if the new file already exists
                if not os.path.exists(new_filepath):
                    print(f"{extension} file missing for {filepath}")

    # If path is a file, process the single file
    elif os.path.isfile(path):
        # Create a new filename with extension
        new_filename = os.path.splitext(os.path.basename(path))[0] + '.' + extension
        new_filepath = os.path.join(os.path.dirname(path), new_filename)
        # Check if the new file already exists
        if not os.path.exists(new_filepath):
            print(f"{extension} file missing for {path}")

    # If path does not exist, print an error message
    else:
        print(f"Error: {path} does not exist.")

if __name__ == '__main__':

    # Define the arguments
    parser = argparse.ArgumentParser(description='Create captions for files.')
    parser.add_argument('-i', '--input-dir', help='The file path or directory.', required=True)
    parser.add_argument('-f', '--force', action='store_true', help='Force overwriting existing caption files.')
    parser.add_argument('-l', '--list-missing', action='store_true', help='List all files that do not have a matching caption file.')
    parser.add_argument('-e', '--extension', default='txt', help='Sets a specific file extension, defaults to \"txt\"')

    # Parse the args
    args = parser.parse_args()

    # Set allowed images for directory scan (Sorry GIF)
    # TODO: make this work. Currently all files are matched
    # switch os walking to alternative function for recursive walk or not
    file_filter = ('jpeg','jpg','png','bmp','webp')

    # if list missing files, do that only.
    if args.list_missing:
        list_missing_captions(args.input_dir, extension=args.extension)
    else:
        create_caption(args.input_dir, args.force)