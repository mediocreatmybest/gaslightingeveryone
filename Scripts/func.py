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

def list2String(list):
    """initialize a list into seperated string"""
    seperator = ", "
    #return string
    return (seperator.join(list))

def list2String_space_sep(list):
    """initialize a list into space seperated string"""
    seperator = " "
    #return string
    return (seperator.join(list))