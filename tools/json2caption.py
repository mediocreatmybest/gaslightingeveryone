import os
import argparse
import json
import re
from pathlib import Path

# Create the parser options
parser = argparse.ArgumentParser(description='Process JSON files.')
parser.add_argument('directory', type=str, help='the directory to search for JSON files')
parser.add_argument('--write-mode', type=str, help='how to treat existing data if found', choices=['append', 'write', 'prepend'], default='write')
parser.add_argument('--keys', type=str, help='the keys to extract (comma-separated)', default='tags')
parser.add_argument('--order-by', type=str, help='the order to output keys (comma-separated)')
parser.add_argument('--output-file', type=str, help='the name of the output file')
parser.add_argument('--output-folder', type=str, help='the folder to save the output file')
parser.add_argument('--output-extension', type=str, help='the extension of the output file', choices=['txt', 'tags', 'caption'], default='tags')
parser.add_argument('--filter', type=str, help='simple list of text to remove from output, accepts regex pattern, (comma-separated)')
parser.add_argument('--filter-file', type=str,
                    help='alternative list of text to remove from output, (each new line is a separate filter), this option only filters json values')
parser.add_argument('--regex-filter-file', type=str,
                    help='alternative regex list of text to remove from output, (each new line is a separate filter), this option only filters json values')
parser.add_argument('--word-swap', type=str,
                    help='text file with word swap pairs, useful for unwanted key values, (each new line is a colon separate pair), this option only swaps json values')
parser.add_argument('--underscore-to-space', type=str, help='converts underscores to spaces in output', choices=['yes', 'no'], default='yes')
parser.add_argument('--debug', action='store_true', help='disables saving files, prints output and save location')

def search_files(directory):
    """Searches for JSON files in the specified directory"""
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


def image_hunt(root_path, base_name, extensions=('jpg', 'jpeg', 'png', 'bmp', 'webp')):
    # We are going on a bear, err, image hunt, we are going to catch a big one, we're not scared
    """Searches for image files in the specified directory"""
    for root, dirs, files in os.walk(root_path):
        for file in files:
            file_base, file_ext = os.path.splitext(file)
            if file_base == base_name and file_ext.lower().lstrip('.') in extensions:
                return os.path.join(root, file)
    return None


# from: https://hackersandslackers.com/extract-data-from-complex-json-python/
def json_extract(obj, key):
    """ Recursively fetch values from nested JSON """
    arr = []

    def extract(obj, arr, key):
        """ Recursively search for values of key in JSON tree """
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

def read_keys(json_data, keys):
    """Reads the specified keys from the JSON data"""
    result = {}
    for key in keys:
        key_parts = key.split('.')
        value = json_data
        for part in key_parts:
            if isinstance(value, list):
                # if the current value is a list, recursively call read_keys on each element in the list
                value = [read_keys(elem, [part]) for elem in value]
                value = [elem for elem in value if elem is not None]
                break
            elif isinstance(value, dict) and part in value:
                # if the current value is a dictionary, traverse the dictionary as before
                value = value[part]
            else:
                value = None
                break
        result[key] = value
    return result


def extract_keys(json_files, keys, encoding='utf-8', debug=False):
    """Extracts the specified keys from the JSON files"""
    results = []
    for file in json_files:
        with open(file, 'r', encoding=encoding) as f:
            json_data = json.load(f)

            result = read_keys(json_data, keys)
            result['_filename'] = os.path.basename(file)
            result['_rootpath'] = os.path.abspath(os.path.dirname(file))
            # try to extract the extension from json_data
            try:
                result['_extension'] = json_extract(json_data, 'extension')[0]
            except IndexError:
                result['_extension'] = None
            if debug is True:
                print("Debug: ", result['_filename'])
                print("Debug: ", result['_rootpath'])
                print("Debug: ", result['_extension'])
            results.append(result)
    return results


def format_output(results, order_by):
    """Formats the output in the specified order"""
    output = ''
    for result in results:
        line = ''
        for key in order_by:
            # check if key is in result and if the value is not empty or None or []
            if key in result and result[key] not in ['', None, []]:
                value = result[key]
                # if the value is a list, check if any of its elements are not empty or None
                if isinstance(value, list):
                    values = [v for v in value if v not in ['', None]]
                    # if there are non-empty values, join them with commas
                    if values:
                        value = ', '.join(values)
                    # if there are no non-empty values, skip this key-value pair
                    else:
                        continue
                # if the value is a dictionary, recursively call format_output with the dictionary's keys as the order_by argument
                elif isinstance(value, dict):
                    value = format_output([value], value.keys())
                # if the value is a string or number, leave it as is
                if line:
                    line += ', '
                # add the key-value pair to the line string
                line += f'{key}: {value}'
        # add the line string to the output string
        if line:
            if output:
                output += ', '
            output += line
    return output


def save_output(output, output_file, output_folder, write_mode='w', prepend_output=False, single_file_mode=False, debug=False):
    """
    Saves the output to a file, prepending, appending, or overwriting the file as specified from args.

    args:
        output (str):               The output string to be saved to the file.
        output_file (str):          The name of the file to save the output to.
        output_folder (str):        The path to the folder where the file will be saved.
        write_mode (str):           The mode to open the file in for writing.
                                    'w' for write mode, 'a' for append mode, defaults to 'w'.
        prepend_output (bool):      If True, prepend the output to the file separated by a comma.
                                    Default is False.
        debug (bool):               If True, prints output and save location without saving the file.
                                    Default is False.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create the full path to the output file
    output_file = os.path.join(output_folder, output_file)

    # Check if the output file already exists
    if os.path.exists(output_file):
        # If the file exists and prepend_output is True, read the existing content,
        # open the file in write mode, and prepend the output string
        if prepend_output:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
                existing_content.strip(',')
            if debug:
                print(f"Appending to file '{output_file}':\n{output + ', ' + existing_content}")
            else:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(output + ', ' + existing_content)
        # If the file exists and write_mode is 'a', open it in append mode and
        # append the output string
        elif write_mode == 'a':
            if debug:
                print(f"Appending to file '{output_file}':\n{output}")
            else:
                with open(output_file, 'a', encoding='utf-8') as f:
                    # If single_file_mode is True, don't add a comma before the output string
                    if single_file_mode is True:
                        f.write(output)
                    else:
                        f.write(', ' + output)
        # If the file exists and write_mode is 'w', open it in write mode and
        # overwrite the existing content with the output string
        elif write_mode == 'w':
            if debug:
                print(f"Overwriting file '{output_file}':\n{output}")
            else:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(output)
        else:
            raise ValueError("Invalid write mode. Must be 'w' or 'a'.")
    else:
        # If the file doesn't exist, create it and write the output string
        if debug:
            print(f"Creating file '{output_file}' with content:\n{output}")
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)


def filter_output(output, filter_text):
    """Filters the output using regex"""
    if filter_text:
        pattern = '|'.join(filter_text.split(','))
        output = re.sub(pattern, '', output)
    return output


def filter_file(output, filter_file):
    """
    Simple filter that reads from a text file to remove text from string.
    It should include any and all text that needs to be removed from the output including spaces and punctuation.

    args:
            output (str): The string to be filtered.
            filter_file (str): The path to the text file containing filters to be removed from the string.

    returns:
            str: The filtered string.
    """
    with open(filter_file, 'r', encoding='utf-8') as f:
        filters = f.read().splitlines()
    for word in filters:
        output = output.replace(word, '')
    return output


def word_swap(output, replacements_file):
    """
    Word swap function, reads a text file containing pairs of words to be replaced in the output string.
    Word pairs are seperated by a colon and on each new line.
    e.g.    'cat:Super cat'
            'bob:Super bob'
    args:   output (str): The string to be filtered.
            replacements_file (str): The path to the text file containing filters to be removed from the string.
    returns: str: The word swaped string.
    """
    # Read the replacement pairs from the file
    with open(replacements_file, 'r') as f:
        replacement_lines = f.readlines()
        replacements = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in replacement_lines}

    # Replace specific lines of text
    for line, replacement in replacements.items():
        # Match only whole words in the line
        pattern = r'\b{}\b'.format(line)
        output = re.sub(pattern, replacement, output)

    return output


def regex_filter_file(output, filter_file):
    """
    Filter text from a string using regular expressions read from a text file.

    args:       output (str): The string to be filtered.
                filter_file (str): The path to the text file containing regular expression patterns

    returns:    str: The filtered string.
    """
    with open(filter_file, 'r', encoding='utf-8') as f:
        filters = f.read().splitlines()
    for pattern in filters:
        output = re.sub(pattern, '', output)
    return output


def main():
    args = parser.parse_args()

    # Set some defaults for args
    # if no keys are specified for order_by use the keys argument
    if args.order_by is None:
        args.order_by = args.keys

    # search for JSON files
    json_files = search_files(args.directory)

    # extract specified keys from the JSON files
    keys = [key.strip() for key in args.keys.split(',')] if args.keys else None
    # get the result of the extraction as a list of dictionaries
    results = extract_keys(json_files, keys)

    # format the output
    order_by = [key.strip() for key in args.order_by.split(',')] if args.order_by else None
    output = format_output(results, order_by)

    # For each result, filter the output and save it to a file
    for result in results:
        output = format_output([result], order_by)
        # filter the output
        output = filter_output(output, args.filter)

        # Set the output file and folder if needed
        if args.output_file:
            output_file = args.output_file
            output_folder = args.output_folder

        # If no output file is specified, we need to create one based on the JSON file name
        else:
            output_file = os.path.splitext(result['_filename'])[0] + f'.{args.output_extension}'
        # If no output folder is specified, we need to use the root path of the JSON file
        # Otherwise, we use the output folder specified
        if args.output_folder:
            output_folder = args.output_folder
        else:
            output_folder = Path(result['_rootpath'])

        # set the write mode
        if args.write_mode == 'append':
            write_mode = 'a'
            prepend_output = False
        if args.write_mode == 'write':
            write_mode = 'w'
            prepend_output = False
        if args.write_mode == 'prepend':
            write_mode = 'w'
            prepend_output = True

        # Check if we need to do additional filtering from a filter file
        if args.filter_file:
            output = filter_file(output, args.filter_file).strip(',')

        # Check if we need to do additional word swaps from a dictionary file
        if args.word_swap:
            output = word_swap(output, args.word_swap).strip()

        # Check if we need to do additional regex filtering from a filter file
        if args.regex_filter_file:
            output = regex_filter_file(output, args.regex_filter_file)
            output = output.strip()
            output = output.strip(',')

        # Check if we need to replace underscores with spaces
        if args.underscore_to_space == 'yes':
            output = output.replace('_', ' ')
        if args.underscore_to_space == 'no':
            # maybe do something different next time
            pass

        # final cleanup of the output string, maybe...
        output = output.replace(',, ',', ')
        output = output.strip(',')

        if args.output_file:
            if result['_extension'] is None:
                basename = os.path.splitext(result['_filename'])[0]
                # hunt for the image file, if it exists
                found_image = image_hunt(result['_rootpath'], basename)
                # if no image is found, set the extension to jpg because why not
                # this shouldn't happen and I'm tired of thinking of 'what if' scenarios
                if found_image is None:
                    result['_extension'] = 'jpg'
                else:
                    # split the found image into a name and extension
                    imagename, extension = os.path.splitext(found_image)
                    # Set extension to the found image extension
                    result['_extension'] = extension.lstrip('.')
            # create image name to append to the output file as faux csv style output for some data loaders
            append_file_name = os.path.splitext(result['_filename'])[0] + '.' + result['_extension']
            output = append_file_name + ', ' + output + '\n'
            # enable single file output for save_output
            single_file_mode=True
        else:
            single_file_mode=False

        # save the output to a file
        save_output(output, output_file, output_folder, write_mode=write_mode,
                    prepend_output=prepend_output,single_file_mode=single_file_mode,
                    debug=args.debug)

if __name__ == '__main__':

# Pew pew! Fire in the hole! Needs additional work with key extraction and subkeys!
    main()