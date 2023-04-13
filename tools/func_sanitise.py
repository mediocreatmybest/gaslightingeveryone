import os
import re


def sanitise_char(char_string, debug=False):
    """ Removes unwanted characters and extensions from a string
        useful for moving files from Linux to Windows and back
    """

    # Add additional characters if needed
    invalid_chars = r'\\/:*?"\'<>|'
    new_char_string = ''.join(c for c in char_string if c not in invalid_chars)

    # Simple print debug
    if debug:
        if char_string != new_char_string:
            print(f"Filter used: \"{invalid_chars}\" to remove invalid characters from name: \"{char_string}\" -> \"{new_char_string}\"")
        else:
            print(f"No invalid characters found in name: \"{char_string}\"")

    # returns string with characters removed and redundant extensions removed, otherwise returns unmodified string
    return new_char_string


def sanitise_double_ext(filename, ext_to_remove=None, debug=True):
    """ Remove an unwanted file extension(s) from a list
        otherwise it "should" return the unmodified filename.
    """
    if not filename or not ext_to_remove:
        if debug:
            print(f"No changes made to: {filename}")
        return filename

    # regex for the list of extensions to remove with for loop over list
    ext_pattern = '|'.join(re.escape(ext) for ext in ext_to_remove)
    if debug:
        print(f"Extensions pattern: {ext_pattern}")

    # good old re.sub to match and remove the extensions
    modified_filename = re.sub(f'({ext_pattern})+', '', filename)
    if debug:
        print(f"Filename without extensions: {modified_filename}")

    # add the file extension back if it was removed
    last_ext = re.search(f'({ext_pattern})$', filename)
    if last_ext and not re.search(f'({ext_pattern})$', modified_filename):
        modified_filename += last_ext.group()
        if debug:
            print(f"Extension added back: {last_ext.group()}")

    if debug:
        print(f"Final sanitised filename: {modified_filename}")

    return modified_filename


def create_captions(file_path, ext="txt", force=False, debug=False, encoding="utf-8"):
    """ Create captions with each file, we are ignore filtering, this can be done in the main() """
    base_name, _ = os.path.splitext(os.path.basename(file_path))
    caption_file_path = os.path.join(os.path.dirname(file_path), f"{base_name}.{ext}")

    if os.path.exists(caption_file_path) and not force:
        if debug:
            print(f"Caption file already exists for {file_path}: {caption_file_path}")
        # File exists, return True and exit
        return True
    # Try open file and write base name, print error if debug is enabled
    try:
        with open(caption_file_path, 'w', encoding=encoding) as f:
            f.write(base_name)
    except Exception as e:
        if debug:
            print(f"Error creating caption file for {file_path}: {str(e)}")
        return False

    if debug:
        print(f"Caption file created for {file_path}: {caption_file_path}")

    return True