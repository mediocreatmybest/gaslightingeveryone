import argparse
import os
from os.path import splitext

from transformers import pipeline

from func_os_walk_plus import os_walk_plus

# An attempt to make simple captions to text in a recursive way using pipeline with Transformers

CAPTION_MODELS = {
    'blip-base': 'Salesforce/blip-image-captioning-base',
    'blip-large': 'Salesforce/blip-image-captioning-large',
    'blip2-2.7b': 'Salesforce/blip2-opt-2.7b',
    'blip2-flan-t5-xl': 'Salesforce/blip2-flan-t5-xl',
    'vit-gpt2-coco-en':'ydshieh/vit-gpt2-coco-en',
}

# Simple non-batched caption
def caption_image(captioner, image_path):
    caption = captioner(image_path)[0]['generated_text']
    print(image_path, caption)
    return caption

# Enable write,append,prepend,skip options
def save_file(file_path, data, encoding='utf-8', mode='write', skip=False, separators=True, debug=False):
    # Check if debug mode is enabled
    if debug:
        print("Save location:", file_path)
        print("Mode:", mode)
        return

    # Check if skip mode is enabled and the file already exists
    if skip and os.path.exists(file_path):
        return

    # Check write mode
    if mode == 'write':
        file_mode = 'w'  # Overwrite/create new file
    elif mode == 'prepend':
        file_mode = 'r+'  # Read/write, to prepend file
    elif mode == 'append':
        file_mode = 'a'  # Append the file
    else:
        raise ValueError("Error beep boop! Select 'write', 'prepend', 'append'")

    # Check if the file exists
    file_exists = os.path.exists(file_path)

    # Open with encoding
    with open(file_path, file_mode, encoding=encoding) as file:
        # Prepend mode, set separators to only exist
        if mode == 'prepend':
            if separators:
                separator = ', ' if file_exists else ''
            else:
                separator = ' ' if file_exists else ''
            file.seek(0)  # Move file pointer to the beginning
            existing_data = file.read()
            file.seek(0)  # Move file pointer to the beginning
            file.write(f"{data}{separator}{existing_data}")

        # Append mode
        elif mode == 'append':
            if separators:
                separator = ', ' if file_exists else ''
            else:
                separator = ' ' if file_exists else ''
            file.write(f"{separator}{data}")

        # Write mode is default
        else:
            file.write(data)


def main():
    parser = argparse.ArgumentParser(description='Caption images with Transformers Pipeline')
    parser.add_argument('directory', type=str,
                        help='Directory to search for images')
    parser.add_argument('--depth', type=int, metavar='1',
                        help='Sets how deep to travel into folders, defaults to full, 1, 2, 3, etc.', default=None)
    parser.add_argument('--mode', type=str, choices=['write', 'append', 'prepend'], default='write',
                        help='Sets the write mode to use when existing captions are found')
    parser.add_argument('--skip-existing', action='store_true',
                        help='Skip existing files if found')
    parser.add_argument('--ext', type=str, default='txt', metavar='txt or caption',
                        help='Extension for the caption files')
    parser.add_argument('--cpu-offload', action='store_true',
                        help='Switches to CPU')
    parser.add_argument('--model', type=str, choices=list(CAPTION_MODELS.keys()), default='blip-large',
                        help='Model to use for captioning')
    parser.add_argument('--max-tokens', type=int, default=25, metavar='25',
                        help='The maximum number of tokens for the model')
    args = parser.parse_args()

    # Load pipeline / model
    # Maybe switch to list and store captions and zip them with file in future, note - look up batch
    if args.cpu_offload:
        device = "cpu"
    else:
        device = None

    # Pipeline example from hugging face
    captioner = pipeline("image-to-text", model=CAPTION_MODELS[args.model], max_new_tokens=args.max_tokens, device=device, use_fast=True)

    # Use os walk plus to allow depth and file filtering
    for path, _, files in os_walk_plus(args.directory, file_filter=('.jpg', '.jpeg', '.png', '.webp'), max_depth=args.depth):
        for file in files:
            image_path = os.path.join(path, file)
            base_file = splitext(image_path)[0]
            caption = caption_image(captioner, image_path)
            full_path = f"{base_file}.{args.ext}"
            save_file(full_path, data=caption, mode=args.mode, skip=args.skip_existing)

if __name__ == "__main__":
    main()