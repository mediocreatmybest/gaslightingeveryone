import argparse
import numpy as np

from pathlib import Path
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS

# txt2wordcloud - examples used from https://towardsdatascience.com/how-to-create-beautiful-word-clouds-in-python-cfcf85141214

# Create the arg parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--inputfile', type=str,
                    help='Text file with all your words', metavar='c:\captions\allcaptions.txt', required=True)
parser.add_argument('--outputfile', type=str,
                    help='Image file to save', metavar='c:\images\wordcloud.png', required=True)
parser.add_argument('--mask', type=str,
                    help='PNG mask for the wordcloud', metavar='c:\captions', required=False)
parser.add_argument('--maxwords', type=int,
                    help='Maximum words to use in the wordcloud', default=250, metavar='250', required=False)
# Add debug option to help disable save and prints out useful variables
#parser.add_argument('--debug', action='store_true',
#                    help='Disables Saving files, prints output locations', required=False)

# Parse the argument
cmd_args = parser.parse_args()

INPUT_FILE = Path(rf"{cmd_args.inputfile}")
OUTPUT = Path(rf"{cmd_args.outputfile}")
MASK = Path(rf"{cmd_args.mask}")

# Open the file and read its contents
with open(INPUT_FILE, 'r', encoding='utf-8') as file:
    words = file.read()

#Define a list of stop words, You can switch STOPWORDS with mystopwords and define your own list.
mystopwords = ['a', 'is', 'you', 'of', 'in', 'to', 'too']

#A function to generate the word cloud from text
def generate_colormask_wordcloud(data, mask=None):
    cloud = WordCloud(scale=2,
                      max_words=cmd_args.maxwords,
                      color_func=colors,
                      mask=mask,
                      background_color='white',
                      stopwords=STOPWORDS,
                      collocations=False,
                      contour_color='#5d0f24',
                      # Optional: You can swap out and list your own font
                      #font_path='C:\\images\\masks\\Aquire-BW0ox.otf',
                      contour_width=3).generate_from_text(data)
    return(cloud)

#A function to generate the word cloud from text
def generate_colormap_wordcloud(data, mask=None):
    cloud = WordCloud(scale=2,
                      max_words=cmd_args.maxwords,
                      colormap='RdYlGn',
                      mask=mask,
                      background_color='white',
                      stopwords=STOPWORDS,
                      collocations=False,
                      contour_color='#5d0f24',
                      # Optional: You can swap out and list your own font
                      #font_path='C:\\images\\masks\\Aquire-BW0ox.otf',
                      contour_width=3).generate_from_text(data)
    return(cloud)

# Check if a mask has been used.
if cmd_args.mask is None:
    # Generate wordcloud
    wordcloud_image = generate_colormap_wordcloud(words).to_image()
else:
    OPEN_MASK = np.array(Image.open(MASK))
    #Grab the mask color for color mask
    colors = ImageColorGenerator(OPEN_MASK)
    # Generate wordcloud with mask, Optional: Switch to colour mask to use colours from your mask
    wordcloud_image = generate_colormap_wordcloud(words, OPEN_MASK).to_image()

# Save final output with PIL
wordcloud_image.save(OUTPUT)