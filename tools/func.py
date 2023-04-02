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


def walk_path(path, ext_filter, recursive_level='full'):
    """ Walks through a folder and returns a list of files with a specific extension.

    Args:
        folder (path)
        ext (list): list of extensions to filter for

    Returns:
        list: list with full path
    """
    # Set this based on function input but easier to read (for me)
    if recursive_level == 'full':
        depth = int('-1')
    else:
        # Assume it will be an integer
        depth = int(recursive_level)

    return [os.path.join(root, name)
            for root, dirs, files in walklevel(path, depth)
            for name in files
            if name.endswith(tuple(ext_filter))]


def walk_path_plus(path, ext_filter, recursive=True):
    """ Walks through a folder and returns a list of files with a specific extension, supports disabling recursive.

    Returns:
        list: list with full path

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


def concat_files(input_dir, output_dir=None, extensions=[], output_ext='txt'):
    """
    Finds and joins text files
    args:   input_dir, input directory
            output_dir, output directory, defaults to the same directory as the input files
            extensions, extensions of files to find, txt, tags, etc.
            output_ext, extension of file to save
    """
    files = walk_path(input_dir, extensions)
    for file in files:
        with open(file, 'r', encoding="utf-8") as input_file:
            contents = input_file.read()
            if output_dir is None:
                output_dir = os.path.dirname(file)
            output_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file))[0] + '.' + output_ext)
            with open(output_file_path, 'a', encoding="utf-8") as output_file:
                if os.stat(output_file_path).st_size > 0:
                    output_file.write(', ')
                output_file.write(contents)