import json
import re

def has_nested_keys(json_obj, keys):
    """
    Returns True if any of the specified keys in the JSON object has nested keys, False otherwise.
    """
    if isinstance(json_obj, str):
        json_obj = json.loads(json_obj)
    if not isinstance(json_obj, dict):
        return False
    for key in keys:
        if isinstance(key, list):
            new_key = ".".join(key)
        else:
            new_key = key
        if new_key not in json_obj:
            continue
        if isinstance(json_obj[new_key], dict):
            return True
    return False


def list2string(lst):
    """initialize a list into separated string"""
    # Check if tags are separated by comma or space
    if all("," in tag for tag in lst):
        separator = ", "
    else:
        separator = " "
    # Return string
    return separator.join(lst)

def nestedkeys2list(data, keys, subcategories=None):
    """
    Returns a list of values from the specified nested keys and subcategories.
    """
    if isinstance(data, str):
        data = json.loads(data)

    values = []
    for key in keys:
        if key in data:
            if subcategories is None:
                values.extend(data[key])
            else:
                subcategories_values = []
                if isinstance(data[key], dict):
                    for subcategory in subcategories:
                        if subcategory in data[key]:
                            subcategories_values.extend(data[key][subcategory])
                values.extend(subcategories_values)
    return values


def string2list(string):
    lst = []
    # check if string is separated by comma or space
    if "," in string:
        delimiter = ","
    else:
        delimiter = None
    # split string into list
    for word in string.split(delimiter):
        lst.append(word.strip())

    return lst

def get_output(data, primary_keys, selected_subcategories=None):
    """
    Returns a list of values from the specified nested keys and subcategories in the desired order.
    """
    output_order = ["Key1", "tags", "key2", "other_tag"]
    output_dict = {}

    if has_nested_keys(data, primary_keys):
        if selected_subcategories is None:
            selected_subcategories = []
        output_dict = {
            key: nestedkeys2list(data, [key], selected_subcategories) for key in primary_keys
        }

    for key in primary_keys:
        if key in data:
            value = data[key]
            if isinstance(value, str):
                output_dict[key] = string2list(value)
            elif isinstance(value, list):
                output_dict[key] = value

    # Rearrange output in desired order
    output = []
    for key in output_order:
        if key in output_dict:
            if isinstance(output_dict[key], list):
                values = list2string(output_dict[key])
            else:
                values = output_dict[key]
            output.append(f"{key.title()}: {values}")
    return output


# Load JSON
with open('input1.json') as f:
    data = json.load(f)

# create lists
output = []
selected_subcategories = []
primary_keys = []

primary_keys = input("Enter a comma-separated list of primary keys to search: ").split(",")
if has_nested_keys(data, primary_keys):
    selected_subcategories = input("Enter a comma-separated list of subcategories to include or leave blank if none: ").split(",")

output.extend(get_output(data, primary_keys, selected_subcategories))
print(output)
