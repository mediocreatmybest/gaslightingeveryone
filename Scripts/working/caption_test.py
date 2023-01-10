import csv
import os
import re
import argparse
from IPython.display import clear_output, display
from PIL import Image
from tqdm import tqdm
from pathlib import Path
from tqdm import tqdm
from clip_interrogator import Config, Interrogator


def sanitize_for_filename(prompt: str, max_len: int) -> str:
    """from:
    https://colab.research.google.com
    /github/pharmapsychotic/clip-interrogator
    /blob/main/clip_interrogator.ipynb
    """
    name = "".join(c for c in prompt if (c.isalnum() or c in ",._-! "))
    name = name.strip()[:(max_len-4)] # extra space for extension
    return name

# Create the arg parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--imagedir', type=str, help='Directory with captions', metavar='c:\images', required=True)
parser.add_argument('--prompt-mode', type=str, choices=['best, fast'], help='best or fast options', metavar='fast', required=False)
parser.add_argument('--output-mode', type=str, choices=['txt, rename, csv, json'], default='txt',
                    help='txt will output txt files, rename will rename files',
                    metavar='fast', required=False)
# Debug
parser.add_argument('--debug', action='store_true', help='Disables Saving files, prints output locations', required=False)

# Parse the argument
cmd_args = parser.parse_args()

# Path to caption files.
captions_path = Path(rf"{cmd_args.imagedir}")

# Full path to our images in a list
full_path_images = []
# Create list for prompts
prompts = []


for root, dirs, files in os.walk(captions_path):
    for file in files:
        if file.endswith('.jpg'):
            image_file = (os.path.join(root, file))
            full_path_images.append(image_file)
            #caption_base_dir = (os.path.join(root))

for index, file in enumerate(tqdm(files, desc='Generating prompts')):
    if index > 0 and index % 100 == 0:
        clear_output(wait=True)
    image = Image.open('c:\\images\\bird.jpg').convert('RGB')
    #ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
    ci = Interrogator(Config(clip_model_name="ViT-B-32/openai"))
    #ci = Interrogator(Config(clip_model_name="ViT-H-14/laion2b_s32b_b79k"))
    #ci = Interrogator(Config(clip_model_name="xlm-roberta-large-ViT-H-14/frozen_laion5b_s13b_b90k"))
    print(ci.interrogate(image))
    #prompts.append(prompt)


