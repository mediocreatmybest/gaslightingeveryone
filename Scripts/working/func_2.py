import pathlib

# Function to extract nested json data,
# https://hackersandslackers.com/extract-data-from-complex-json-python/
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


# Function to convert tags to string
def list2String(convertlist):
    """initialize a list into seperated string"""
    seperator = ", "
    #return string
    return (seperator.join(convertlist))

def list2String_space_sep(convertlist):
    """initialize a list into space seperated string"""
    seperator = " "
    #return string
    return (seperator.join(convertlist))

# Function to help cocatenate simple txt files
def concatenate_files(root_dir, output_file):
    """ Function to concatenate text files into a single file  """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_path in pathlib.Path(root_dir).glob('**/*.txt'):
            with open(file_path, 'r', encoding='utf-8') as infile:
                # Concatenate the contents of the file to the output file
                outfile.write(infile.read() + ' ')

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