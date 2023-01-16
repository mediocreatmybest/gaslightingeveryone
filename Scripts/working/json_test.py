import json
import argparse

# Cmd line arg

parser = argparse.ArgumentParser()
parser.add_argument('--json', help='Location of Json', required=True)
parser.add_argument('--key', help='Filter by JSON key or keys', metavar='id username fullname', nargs='+', required=True)
args = parser.parse_args()

# Key Filter
key_filter = (args.key)

# Parse JSON
with open (args.json, "r", encoding='utf-8') as json_file:
    data = json.load(json_file)

# Define Recurse Lookup this will only will output the first value matching a key
def recursive_search(data, fkey):
    filtered_data={}
    for k, v in data.items():
        if isinstance(v,dict):
            filtered_data.update(recursive_search(v, fkey))
        elif k in fkey:
            filtered_data[k] = v
    return filtered_data


filtered_data = recursive_search(data, fkey=key_filter)

# I want just user names:
for key, value in filtered_data.items():
    if key == 'username':
        print(f'the key is:"{key}" and the value is "{value}"')

