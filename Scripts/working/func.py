import codecs
import os

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
    with codecs.open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with codecs.open(file_path, 'r', encoding='utf-8') as infile:
                        # Concatenate the contents of the file to the output file
                        outfile.write(infile.read())
                        # Space seperator
                        outfile.write(' ')
# Walklevel function
# MIT License
#
# Copyright (c) 2021 Matthew Schweiss
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Partially from https://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
# https://gist.github.com/TheMatt2/faf5ca760c61a267412c46bb977718fa

import os

def walklevel(path, depth = 1):
    """It works just like os.walk, but you can pass it a level parameter
       that indicates how deep the recursion will go.
       If depth is 1, the current directory is listed.
       If depth is 0, nothing is returned.
       If depth is -1 (or less than 0), the full depth is walked.
    """
    # If depth is negative, just walk
    # Not using yield from for python2 compat
    # and copy dirs to keep consistant behavior for depth = -1 and depth = inf
    if depth < 0:
        for root, dirs, files in os.walk(path):
            yield root, dirs[:], files
        return
    elif depth == 0:
        return

    # path.count(os.path.sep) is safe because
    # - On Windows "\\" is never allowed in the name of a file or directory
    # - On UNIX "/" is never allowed in the name of a file or directory
    # - On MacOS a literal "/" is quitely translated to a ":" so it is still
    #   safe to count "/".
    depth -= 1
    base_depth = path.rstrip(os.path.sep).count(os.path.sep)
    for root, dirs, files in os.walk(path):
        yield root, dirs[:], files
        cur_depth = root.count(os.path.sep)
        if base_depth + depth <= cur_depth:
            del dirs[:]


def walk_path(path, ext_filter=None, recursive_level='full'):
    """ Walks through a folder and returns a list of files with a specific extension.

    Args:
        path (str): path to the folder to search.
        ext_filter (list): list of extensions to filter for. If set to None, all files will be returned.
        recursive_level (str or int): specifies the depth of the directory tree to search. If set to 'full', the entire directory tree will be searched. If set to a non-negative integer, the search will be limited to that many levels deep.

    Returns:
        list: a list of full file paths.
    """
    if recursive_level == 'full':
        depth = -1
    else:
        # should force string to int if string is a number
        depth = int(recursive_level)

    if ext_filter is None:
        ext_filter = []

    return [os.path.join(root, name)
            for root, dirs, files in walklevel(path, depth)
            for name in files
            if len(ext_filter) == 0 or name.endswith(tuple(ext_filter))]


def oswalk_plus(top, recursive=False):
    """ It works just like os.walk, but you can pass it a recursive parameter
        that indicates if you want to curse at subdirectories. """
    dirs = []
    nondirs = []
    for name in os.listdir(top):
        if os.path.isdir(os.path.join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)
    yield top, dirs, nondirs
    if recursive:
        for name in dirs:
            path = os.path.join(top, name)
            yield from oswalk_plus(path, recursive)


def walk_path_plus(path, ext_filter, recursive=True):
    """ Walks through a folder and returns a list of files with a specific extension, supports disabling recursive.

    Returns: list: list with full path

    """
    return [os.path.join(root, name)
            for root, dirs, files in oswalk_plus(path, recursive)
            for name in files
            if name.endswith(tuple(ext_filter))]


def concat_str(*args):
    """
    concatenates random number strings with a comma separator.

    args: *args: strings to be concatenated.

    returns: A single string with all input strings concatenated together, separated by commas.

    example: concat_str('abc', 'def', 'ghi') returns 'abc, def, ghi'
    """
    return ', '.join(args)

