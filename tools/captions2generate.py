import argparse
import os
from os.path import splitext

from transformers import pipeline
#from optimum.pipelines import pipeline

from func_os_walk_plus import os_walk_plus

# An attempt to make simple captions to text in a recursive way using pipeline with Transformers

CAPTION_MODELS = {
    'blip-base': 'Salesforce/blip-image-captioning-base',
    'blip-large': 'Salesforce/blip-image-captioning-large',
    'blip2-2.7b': 'Salesforce/blip2-opt-2.7b',
    'blip2-opt-6.7b': 'Salesforce/blip2-opt-6.7b',
    'blip2-flan-t5-xl': 'Salesforce/blip2-flan-t5-xl',
    'vit-gpt2-coco-en':'ydshieh/vit-gpt2-coco-en',
}

ZEROSHOT_MODELS = {
    'clip-vit-large-patch14': 'openai/clip-vit-large-patch14',
    'CLIP-ViT-H-14-laion2B-s32B-b79K': 'laion/CLIP-ViT-H-14-laion2B-s32B-b79K',
}


# Simple non-batched caption
def caption_image(captioner, image_path):
    caption = captioner(image_path)[0]['generated_text']
    print('File: ', image_path)
    print('Caption: ', str(caption).strip())
    return str(caption).strip()


# Batch caption attempt, using lists, doesn't seem any faster...
def caption_images_batch(captioner, image_paths):
    captions = captioner(image_paths)
    result = []
    for i, caption in enumerate(captions):
        stripped_caption = str(caption[0]['generated_text']).strip()
        print('File: ', image_paths[i])
        print('Caption: ', stripped_caption)
        result.append(stripped_caption)
    return result


# Zero shot list
def read_zshot(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    return lines

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
    parser.add_argument('--model', type=str, choices=list(CAPTION_MODELS.keys()),
                        help='Model to use for captioning')
    parser.add_argument('--clip-model', type=str, choices=list(ZEROSHOT_MODELS.keys()),
                        help='Model to use for CLIP/Zero Shot Category')
    parser.add_argument('--clip-cat-text', type=str, metavar='/path/textfile.txt',
                        help='File to CLIP/Zero Shot Category file')
    parser.add_argument('--clip-confidence', type=str, default=0.70, metavar='0.70',
                        help='Categories under the confidence score wont be included in final text output')
    parser.add_argument('--max-tokens', type=int, default=25, metavar='25',
                        help='The maximum number of tokens for the caption model')
    parser.add_argument('--batch-count', type=int, metavar='2',
                        help='If you want to try image batch count with pipeline captions')
    args = parser.parse_args()

    if args.clip_model is None and args.model is None:
        print('Please select a model. exiting...')
        exit()

    # Load pipeline / model
    # Maybe switch to list and store captions and zip them with file in future, note - look up batch
    if args.cpu_offload:
        device = "cpu"
    else:
        device = None

    # Convert confidence to a float
    confidence = float(args.clip_confidence)
    # Pipeline example from hugging face
    # Load model if selected
    if args.model:
        print('Loading image-to-text task in pipeline...')
        captioner = pipeline(task="image-to-text", model=CAPTION_MODELS[args.model], max_new_tokens=args.max_tokens, device=device, use_fast=True)

    # Load CLIP zero shot if selected
    if args.clip_model:
        # Read the file and split it line by line
        print('Loading zero-shot-image-classification task in pipeline...')
        zshot_cat = read_zshot(args.clip_cat_text)
        zshot = pipeline(task="zero-shot-image-classification", model=ZEROSHOT_MODELS[args.clip_model], device=device, use_fast=True)

    # Use os walk plus to allow depth and file filtering
    for path, _, files in os_walk_plus(args.directory, file_filter=('.jpg', '.jpeg', '.png', '.webp'), max_depth=args.depth):
        if args.batch_count:
            # Batch processing logic
            batches = [files[i:i+args.batch_count] for i in range(0, len(files), args.batch_count)]
            for batch in batches:
                image_paths = [os.path.join(path, file) for file in batch]
                base_files = [splitext(image_path)[0] for image_path in image_paths]

                # Add caption
                if args.model:
                    captions = caption_images_batch(captioner, image_paths)

                # Only do something if model was selected
                if args.model:
                    for i in range(len(captions)):
                        # Full path to text file to save
                        full_path = f"{base_files[i]}.{args.ext}"
                        # Final caption needs to still be saved for each text file. No batching within text save
                        final_caption = captions[i]
                        save_file(full_path, data=final_caption, mode=args.mode, skip=args.skip_existing)

        # Fall back to single image function
        else:
            # Single image function
            for file in files:
                # Build the caption and append
                build_caption = []
                image_path = os.path.join(path, file)
                base_file = splitext(image_path)[0]

                # Add caption
                if args.model:
                    caption = caption_image(captioner, image_path)
                    build_caption.append(caption)

                # Only do something if model was selected
                if args.model:
                    # Full path to text file to save
                    full_path = f"{base_file}.{args.ext}"
                    # join build_caption and convert to comma string
                    final_caption = ', '.join(build_caption)
                    save_file(full_path, data=final_caption, mode=args.mode, skip=args.skip_existing)

                # Add clip zero shot text
                if args.clip_model:
                    # Start task
                    top_cat = zshot(image_path, candidate_labels=zshot_cat)
                    # We only want items over a specific score
                    for top in top_cat:
                        if top['score'] > confidence:
                            print('Image Category: ', top['label'])
                            build_caption.append(top['label'])
                # Only do something if model or clip_model was selected
                if args.model or args.clip_model:
                    # Full path to text file to save
                    full_path = f"{base_file}.{args.ext}"
                    # join build_caption and convert to comma string
                    final_caption = ', '.join(build_caption)
                    save_file(full_path, data=final_caption, mode=args.mode, skip=args.skip_existing)


if __name__ == "__main__":
    main()