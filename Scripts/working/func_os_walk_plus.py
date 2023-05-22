import os

def os_walk_plus(path, max_depth=None, file_filter=None):
    """
    Recursively go walk about in a directory tree up to a specified maximum depth and optionally filter files by extension.

    Args:   path (str): The root directory to start walking.
            max_depth (int): The maximum depth of directory traversal. If None, traverse the entire directory tree.
            file_filter (str): The file extension to filter files by. If None, all files are included. Defaults to None.

    Yields:     Tuple: To behave like OS Walk we will have three items representing the current directory being walked:
                - root (str): The current directory path.
                - dirs (list): A list of subdirectories in the current directory.
                - files (list): A list of files in the current directory (optionally filtered with file_filter).
    """
    # Initialize a stack with the root directory and depth 0
    stack = [(path, 0)]
    while stack:
        # Pop the next directory from the stack and get its depth
        # Spend my nights with a roll of bubble wrap. POP POP! Hope no one sees me gettin freaky!
        path, level = stack.pop()
        # If max_depth is not None and current level is greater than max_depth, skip traversal
        if max_depth is not None and level > max_depth:
            continue
        # Initialize empty lists for subdirectories and files
        dirs, files = [], []
        try:
            # For loop over the items in the directory
            for name in os.listdir(path):
                # If the item is a subdirectory, add it to the 'dirs' list, else add it to the files list
                if os.path.isdir(os.path.join(path, name)):
                    dirs.append(name)
                else:
                    files.append(name)
        except PermissionError:
            # Skip directories if we aren't allowed to access or peep into
            continue
        # If file_filter is None, yield the entire list of files, else filter by extension
        if file_filter is None:
            yield path, dirs, files
        else:
            filtered_files = [f for f in files if f.endswith(file_filter)]
            yield path, dirs, filtered_files
        # If max_depth is None or current level is less than max_depth, add subdirectories to stack
        if max_depth is None or level < max_depth:
            stack.extend((os.path.join(path, dir), level+1) for dir in dirs)


def os_walk_list(path, max_depth=None, file_filter=None):
    """
    Recursively walk though a directory to a specified maximum depth and optionally filter files by extension,
    returning a list of files, Uses the above os_walk_plus function

    Args:       path (str): The root directory to start traversing.
                max_depth (int): The maximum depth of directory traversal. If None, traverse the entire directory tree.
                file_filter (str): The file extension to filter files by. If None, all files are included. Defaults to None.

    Returns:    List: A list of file paths in the directory tree, optionally filtered by file_filter.
    """
    # Call os_walk_plus
    walk_dir = os_walk_plus(path, max_depth=max_depth, file_filter=file_filter)
    # Jog through the walk_dir and append the files to a list
    files = []
    for root, dirs, walk_files in walk_dir:
        if file_filter is None:
            files.extend(os.path.join(root, file) for file in walk_files)
        else:
            filtered_files = [f for f in walk_files if f.endswith(file_filter)]
            files.extend(os.path.join(root, file) for file in filtered_files)
    # Return final list of files
    return files