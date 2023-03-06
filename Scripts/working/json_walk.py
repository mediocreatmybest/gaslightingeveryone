import os
import json
import argparse

def find_json_files(folder):
    """
    This function takes a folder path as input and returns a list of all the json files in that folder and its subfolders.
    """
    json_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

def read_json_file(file):
    """
    This function takes a json file path as input and returns a dictionary of all the keys and values in that file.
    """
    with open(file, 'r') as f:
        data = json.load(f)
    keys_values = {}
    for key, value in data.items():
        if isinstance(value, dict):
            nested_dict = read_nested_dict(value)
            keys_values.update(nested_dict)
        elif isinstance(value, list):
            nested_list = read_nested_list(value)
            keys_values[key] = nested_list
        else:
            keys_values[key] = value
    return keys_values

def read_nested_dict(data):
    """
    This function takes a dictionary as input and returns a dictionary of all the keys and values in that dictionary and any nested dictionaries.
    """
    nested_keys_values = {}
    for key, value in data.items():
        if isinstance(value, dict):
            nested_dict = read_nested_dict(value)
            for nested_key, nested_value in nested_dict.items():
                nested_keys_values[f'{key}.{nested_key}'] = nested_value
        elif isinstance(value, list):
            nested_list = read_nested_list(value)
            nested_keys_values[key] = nested_list
        else:
            nested_keys_values[key] = value
    return nested_keys_values

def read_nested_list(data):
    """
    This function takes a list as input and returns a list of all the values in that list and any nested lists or dictionaries.
    """
    nested_values = []
    for item in data:
        if isinstance(item, dict):
            nested_dict = read_nested_dict(item)
            nested_values.append(nested_dict)
        elif isinstance(item, list):
            nested_list = read_nested_list(item)
            nested_values.append(nested_list)
        else:
            nested_values.append(item)
    return nested_values

def filter_keys_values(keys_values, primary_keys, subcategory_keys):
    """
    This function takes a dictionary of all the keys and values in a json file and filters it to include only the specified primary keys and subcategory keys and their values.
    """
    filtered_keys_values = {}
    for primary_key in primary_keys:
        if primary_key in keys_values:
            if isinstance(keys_values[primary_key], list):
                filtered_keys_values[primary_key] = []
                for item in keys_values[primary_key]:
                    if isinstance(item, dict):
                        filtered_item = {}
                        for subcategory_key in subcategory_keys:
                            if subcategory_key in item:
                                filtered_item[subcategory_key] = item[subcategory_key]
                        filtered_keys_values[primary_key].append(filtered_item)
            elif isinstance(keys_values[primary_key], dict):
                filtered_keys_values[primary_key] = {}
                for subcategory_key in subcategory_keys:
                    if subcategory_key in keys_values[primary_key]:
                        filtered_keys_values[primary_key][subcategory_key] = keys_values[primary_key][subcategory_key]
            else:
                filtered_keys_values[primary_key] = keys_values[primary_key]
    return filtered_keys_values

def print_keys_values(keys_values, order):
    """
    This function takes a dictionary of all the keys and values in a json file and prints them in the specified order.
    """
    for key in order:
        if key in keys_values:
            if isinstance(keys_values[key], list):
                print(f'{key}:')
                for item in keys_values[key]:
                    if isinstance(item, dict):
                        print_dict(item, 1)
                    else:
                        print(f'  {item}')
            elif isinstance(keys_values[key], dict):
                print_dict(keys_values[key], 0)
            else:
                print(f'{key}: {keys_values[key]}')

def print_dict(data, indent_level):
    """
    This function takes a dictionary as input and prints it recursively with the specified indent level.
    """
    for key, value in data.items():
        if isinstance(value, dict):
            print(f'{"  " * indent_level}{key}:')
            print_dict(value, indent_level + 1)
        elif isinstance(value, list):
            print(f'{"  " * indent_level}{key}:')
            print_list(value, indent_level + 1)
        else:
            print(f'{"  " * indent_level}{key}: {value}')

def print_list(data, indent_level):
    """
    This function takes a list as input and prints it recursively with the specified indent level.
    """
    for item in data:
        if isinstance(item, dict):
            print_dict(item, indent_level + 1)
        elif isinstance(item, list):
            print_list(item, indent_level + 1)
        else:
            print(f'{"  " * indent_level}{item}')

def main():
    parser = argparse.ArgumentParser(description='Read and filter json files.')
    parser.add_argument('folder', type=str, help='the folder to search for json files')
    parser.add_argument('--primary-keys', nargs='+', required=True, help='the primary keys to include in the output')
    parser.add_argument('--subcategory-keys', nargs='+', default=[], help='the subcategory keys to include in the output')
    parser.add_argument('--order', nargs='+', default=[], help='the order to print the keys and values')
    args = parser.parse_args()

    json_files = find_json_files(args.folder)

    for json_file in json_files:
        keys_values = read_json_file(json_file)
        filtered_keys_values = filter_keys_values(keys_values, args.primary_keys, args.subcategory_keys)
        print_keys_values(filtered_keys_values, args.order)

if __name__ == '__main__':
    main()

