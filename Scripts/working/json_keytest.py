import os
import argparse
import json
import re
from pathlib import Path


parser = argparse.ArgumentParser(description='Process JSON files.')
parser.add_argument('directory', type=str, help='the directory to search for JSON files')
parser.add_argument('--keys', type=str, help='the keys to extract (comma-separated)')
parser.add_argument('--order-by', type=str, help='the order to output keys (comma-separated)')
parser.add_argument('--output-file', type=str, help='the name of the output file')
parser.add_argument('--output-folder', type=str, help='the folder to save the output file')
parser.add_argument('--output-extension', type=str, help='the extension of the output file', choices=['txt', 'tags', 'caption'], default='tags')
parser.add_argument('--verbose', action='store_true', help='display output to the screen')
parser.add_argument('--filter', type=str, help='list of text to remove from output')


def search_files(directory):
    """Searches for JSON files in the specified directory"""
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


def read_keys(json_data, keys):
    """Reads the specified keys from the JSON data"""
    result = {}
    for key in keys:
        key_parts = key.split('.')
        value = json_data
        for part in key_parts:
            if part in value:
                value = value[part]
            else:
                value = None
                break
        result[key] = value
    return result


def extract_keys(json_files, keys, encoding='utf-8'):
    """Extracts the specified keys from the JSON files"""
    results = []
    for file in json_files:
        with open(file, 'r', encoding=encoding) as f:
            json_data = json.load(f)
            result = read_keys(json_data, keys)
            result['_filename'] = os.path.basename(file)
            result['_rootpath'] = os.path.abspath(os.path.dirname(file))
            #print("Debug: ", result['_filename'])
            #print("Debug: ", result['_rootpath'])
            results.append(result)
    #print(results)
    return results


def format_output(results, order_by):
    """Formats the output in the specified order"""
    output = ''
    for result in results:
        line = ''
        for key in order_by:
            if key in result and result[key]:
                value = result[key]
                if isinstance(value, list):
                    value = ', '.join(value)
                line += f'{key}: {value}, '
        if line:
            output += line[:-2] + '\n'
    return output


def save_output(output, output_file, output_folder):
    """Saves the output to a file"""

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    output_file = os.path.join(output_folder, output_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)


def filter_output(output, filter_text):
    """Filters the output using regex"""
    if filter_text:
        pattern = '|'.join(filter_text.split(','))
        output = re.sub(pattern, '', output)
    return output


def main():
    args = parser.parse_args()

    # search for JSON files
    json_files = search_files(args.directory)

    # extract specified keys from the JSON files
    keys = [key.strip() for key in args.keys.split(',')] if args.keys else None
    results = extract_keys(json_files, keys)
    print(results)
    # format the output
    order_by = [key.strip() for key in args.order_by.split(',')] if args.order_by else None
    output = format_output(results, order_by)


    # For each result, filter the output and save it to a file
    for result in results:
        output = format_output([result], order_by)
         # filter the output
        output = filter_output(output, args.filter)
        # set the output file name if specified and set the output folder
        if args.output_file:
            output_file = args.output_file
            output_folder = args.directory
            # We need to append the output to itself if we are using the same file name
            # To do this, we need to check if the file exists and if it does, we need to read it
            # and append it to the output - I'm sure this works...it doesn't...
            if os.path.exists(os.path.join(output_folder, output_file)):
                with open(os.path.join(output_folder, output_file), 'r', encoding='utf-8') as f:
                    output = f.read() + "\n" + output
        # If no output file is specified, we need to create one based on the JSON file name
        else:
            output_file = os.path.splitext(result['_filename'])[0] + f'.{args.output_extension}'
        # If no output folder is specified, we need to use the root path of the JSON file
        # Otherwise, we use the output folder specified
        if args.output_folder:
            output_folder = args.output_folder
        else:
            output_folder = Path(result['_rootpath'])

        # then save the output to a file
        save_output(output, output_file, output_folder)

    # display output to the screen in verbose mode
    if args.verbose:
        print(output)

if __name__ == '__main__':
# Pew pew!
    main()