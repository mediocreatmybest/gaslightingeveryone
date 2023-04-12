import os
import re

# Curl shell script

shellscript = 'John_Gould_download.sh'

# File name pattern
file_pattern = r'-o\s+"([^"]+)'

# Magic URL Pattern
url_pattern = r'\b(https?):\/\/([-A-Z0-9.]+)(\/[-A-Z0-9+&@#\/%=~_|!:,.;]*)?(\?[A-Z0-9+&@#\/%=~_|!:,.;]*)?'

# Open the shell script per line, doesn't take into account #!/bin/sh
# but should ignore it as it isn't matched
with open (shellscript, 'r') as f:
    for line in f:

        # Search for the pattern in the script string
        file_search = re.search(file_pattern, line, flags=re.I)
        url_search = re.search(url_pattern, line, flags=re.I)

        if file_search:
            # Get the file name converted to string and URL from the search
            file_name = file_search.group(1)

            # Use os.path to split extension and only use basename from tupple
            file_name = os.path.splitext(file_name)[0]

            # Group the URL together
            url = url_search.group()

            # Save the URL to a text file with the same name as the file being downloaded
            with open(file_name + '.url', 'w') as f:
                f.write(url)