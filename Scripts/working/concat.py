import os
import codecs
from pathlib import Path

con_path = Path(r"c:\images")
out_file = Path(r"c:\output\test.txt")
out_file_dedup = Path(r"c:\output\test-dedup.txt")

def concatenate_files(root_dir, output_file):
  with codecs.open(output_file, 'w', encoding='utf-8') as outfile:
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with codecs.open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())

concatenate_files(con_path, out_file)


# Open the file and read its contents
with open(out_file, 'r', encoding='utf-8') as file:
    contents = file.read()

# Split the contents into a list of words
words = contents.split()

# Convert the list to a set to remove duplicates
words_set = set(words)
sorted_words = sorted(words_set)

# Write the unique words back to the file
with open(out_file_dedup, 'w', encoding='utf-8') as file:
    for word in sorted_words:
        file.write(word + ' ')
