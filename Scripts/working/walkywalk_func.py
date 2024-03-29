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
# walklevel function
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
