import argparse
import os

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

def caption_image(image_path, model, cpu):
    if cpu is True:
        device = "cpu"
    else:
        device = None
    captioner = pipeline("image-to-text", model=CAPTION_MODELS[model], max_new_tokens=50, device=device, use_fast=True)
    caption = captioner(image_path)[0]['generated_text']
    print(image_path, caption)
    return caption

def write_caption_to_file(image_path, caption, mode, ext):
    txt_path = f'{os.path.splitext(image_path)[0]}.{ext}'
    if os.path.exists(txt_path):
        if mode == 'skip':
            return
        elif mode == 'append':
            write_mode = 'a'
            caption = ', ' + caption
        elif mode == 'prepend':
            with open(txt_path, 'r') as txt_file:
                existing_text = txt_file.read()
            caption = caption + ', ' + existing_text
            write_mode = 'w'
        else:  # default is to overwrite
            write_mode = 'w'
    else:
        write_mode = 'w'
    with open(txt_path, write_mode) as txt_file:
        txt_file.write(caption)


def main():
    parser = argparse.ArgumentParser(description='Caption images and write captions to text files')
    parser.add_argument('directory', type=str,
                        help='Directory to search for images')
    parser.add_argument('--depth', type=int, metavar='1',
                        help='Sets how deep to travel into folders, defaults to full, 1, 2, 3, etc.', default=None)
    parser.add_argument('--mode', type=str, choices=['overwrite', 'append', 'prepend', 'skip'], default='overwrite',
                        help='Sets Write mode when existing captions are found')
    parser.add_argument('--ext', type=str, default='txt', metavar='txt or caption',
                        help='Extension for the caption files')
    parser.add_argument('--cpu-offload', action='store_true',
                        help='Switches to CPU')
    parser.add_argument('--model', type=str, choices=list(CAPTION_MODELS.keys()), default='blip-large', help='Model to use for captioning')
    args = parser.parse_args()

    for path, dirs, files in os_walk_plus(args.directory, file_filter=('.jpg', '.jpeg', '.png', '.webp'), max_depth=args.depth):
        for file in files:
            image_path = os.path.join(path, file)
            caption = caption_image(image_path, args.model, args.cpu_offload)
            write_caption_to_file(image_path, caption, args.mode, args.ext)

if __name__ == "__main__":
    main()