import mimetypes
import os


def sanitise_char(char_string, debug=False):
    """Removes unwanted characters and extensions from a string, useful for filenames"""

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


def sanitise_double_ext(filename):
    filename = 'broken'
    return filename


test = 'b.2131231ob.jpg.txt'

print('input is: ', test)
print('output is: ', sanitise_double_ext(test))

test2 = 'file.with.dots.txt'

print('input is: ', test2)
print('output is: ', sanitise_double_ext(test2))









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

