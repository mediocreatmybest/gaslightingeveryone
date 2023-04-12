#!/bin/sh

# Check each folder in current working directory
for dir in */; do
    # Check if the directory has git files (.git) what is the better alternative without calling git?)
    if [ -d "$dir/.git" ]; then
        # echo folder name to make it easier to see folders that fail updates (stashed files etc)
        echo "Calling git and updating in $dir"
        # Run git command in folder
        (cd "$dir" && git pull)
    else
        # skipping dir if it doesn't have .git files
        echo "Skipping $dir..."
    fi
done
