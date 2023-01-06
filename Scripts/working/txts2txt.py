import os
import re
import argparse
from pathlib import Path
from func import concatenate_files, list2String_space_sep

# Create the arg parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--inputdir', type=str,
                    help='Directory with text files', metavar='c:\captions', required=True)
parser.add_argument('--outputfile', type=str,
                    help='Image directory to caption', metavar='c:\captions\allwords.txt', required=True)
parser.add_argument('--dedup', action='store_true',
                    help='Remove all duplicate words', required=False)
# TODO: Create a function for the filter options, make it easier in future to be more selective in what is filtered
#       This would then allow less commandline arguments.
parser.add_argument('--filter', action='store_true',
                    help='Run the regex filter to help remove symbols and whitespace', required=False)
parser.add_argument('--filter-urls', action='store_true',
                    help='Run the regex filter to also remove URLS. This is a sub filter to be used with --filter', required=False)
#parser.add_argument('--write', action='store_true', help='Allow writing or modifying files', required=False)
# Add debug option to help disable save and prints out useful variables
parser.add_argument('--debug', action='store_true',
                    help='Disables Saving files, prints output locations', required=False)

# Parse the argument
cmd_args = parser.parse_args()

con_path = Path(rf"{cmd_args.inputdir}")
out_file = Path(rf"{cmd_args.outputfile}")
out_file_dedup_base = (os.path.splitext(out_file)[0])
out_file_dedup = Path(rf"{out_file_dedup_base}_dedup.txt")
out_file_dedup_filtered = Path(rf"{out_file_dedup_base}_dedup_filtered.txt")

# debug
if cmd_args.debug is True:
    print('Input dir: ', cmd_args.inputdir)
    print('Output file: ', cmd_args.outputfile)
    print('Dedup file is: ', out_file_dedup)
    print('Filtered dedup file is: ', out_file_dedup_filtered)
    print('remove duplicate words: ', cmd_args.dedup)
    print('Filter text is: ', cmd_args.filter)
    print('Filter URLS is: ', cmd_args.filter_urls)
    #print('Write files is: ', cmd_args.write)

# Call and use the concatenate function to combine all text files
concatenate_files(con_path, out_file)

if cmd_args.dedup is True:

    # Open the file and read its contents
    with open(out_file, 'r', encoding='utf-8') as file:
        contents = file.read()
    # Split the contents into a list of words
    words = contents.split()
    # Convert the list to a set to remove duplicates
    words_set = set(words)
    sorted_words = sorted(words_set)

    # Write the unique words back to the file
    with open(out_file_dedup, 'w', encoding='utf-8') as file_dedup:
        for word in sorted_words:
            file_dedup.write(word + ' ')

if cmd_args.filter is True and cmd_args.dedup is True:

    # Convert the list to a string to filter with regex
    filtered_words = list2String_space_sep(sorted_words)

    # Create an exclusion list
    exclusionList = [',', '\|', '–', '&quot;', '&nbsp;', '&amp', '&gt', '"', '”', ' ― ', '- ', ';']
    exclusions = '|'.join(exclusionList)

    # Remove all items in th exclusionList
    filtered_words = re.sub(exclusions, '', filtered_words)
    if cmd_args.filter_urls is True:
        # Remove URLs? Not sure how this magic works.
        filtered_words = re.sub(r'\b(https?):\/\/([-A-Z0-9.]+)(\/[-A-Z0-9+&@#\/%=~_|!:,.;]*)?(\?[A-Z0-9+&@#\/%=~_|!:,.;]*)?','', filtered_words, flags=re.I)

    # Additional filtering
    # White space to get a substitute (teacher) with single (and lonely) space, \s+
    filtered_words = re.sub(r'\s+', ' ', filtered_words)

    with open(out_file_dedup_filtered, 'w', encoding='utf-8') as file_filtered:
        for word in filtered_words:
            file_filtered.write(word)