import argparse
import configparser
import logging
import os
import sys
from os.path import splitext

import torch
from tqdm import tqdm
from transformers import pipeline

from func_os_walk_plus import os_walk_plus
from func_transformers import (CaptionConfig, caption_generate,
                               load_caption_model, pipeline_caption_batch,
                               pipeline_task)

# Set our loggins level to INFO
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Maybe this will work one day.
#from optimum.pipelines import pipeline

# An attempt to make simple captions using pipeline or Transformers
# Find/add/remove additional models. Added some community created models.
CAPTION_MODELS = {
    'blip-base': 'Salesforce/blip-image-captioning-base',
    'blip-large': 'Salesforce/blip-image-captioning-large',
    'blip2-2.7b-coco': 'Salesforce/blip2-opt-2.7b-coco',
    'blip2-2.7b': 'Mediocreatmybest/blip2-opt-2.7b-fp16-sharded',
    'blip2-6.7b': 'ybelkada/blip2-opt-6.7b-fp16-sharded',
    'blip2-6.7b-coco': 'trojblue/blip2-opt-6.7b-coco-fp16',
    'git-base': 'microsoft/git-base',
    'git-large': 'microsoft/git-large',
    'git-base-coco': 'microsoft/git-base-coco',
    'git-large-coco': 'microsoft/git-large-coco',
    'git-large-r-coco': 'microsoft/git-large-r-coco'
}
# Need to find and add additional zshot models that are useful
ZEROSHOT_MODELS = {
    'clip-vit-large-patch14': 'openai/clip-vit-large-patch14',
    'CLIP-ViT-H-14-laion2B-s32B-b79K': 'laion/CLIP-ViT-H-14-laion2B-s32B-b79K',
}


# Zero shot list
def read_zshot(file_path):
    """ Read a file into a list """
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    return lines


# add some docstrings
def zshot_images_batch(zshot, image_paths, candidate_labels, confidence, quiet=False):
    """ Zero shot image classification for a batch of images """
    confidence = float(confidence)  # Make sure this is a float
    classifications = zshot(image_paths, candidate_labels=candidate_labels)
    result = []
    for i, classification in enumerate(classifications):
        high_confidence_labels = [f"{label['label']}" for label in classification if label['score'] > confidence]
        if quiet is False:
            print('\nFile: ', image_paths[i])
            print('Image categories: ', ', '.join(high_confidence_labels))
            print('Score: ', ', '.join([f"{label['score']}" for label in classification if label['score'] > confidence]))
        result.append(high_confidence_labels)
    return result


def does_file_exist(file_path):
    """Simple chceck for file

    Args: file_path

    Returns: yay or nay
    """
    return os.path.exists(file_path)


# Enable write,append,prepend,skip options (remove skip at some point)
def save_file(file_path, data, encoding='utf-8', mode='write', separators=True, debug=False):
    """ saves a file """
    # Check if debug mode is enabled
    if debug:
        print("Save location:", file_path)
        print("Mode:", mode)
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
    """ Main function """

    # Set argparse defaults
    parser = argparse.ArgumentParser(description='Caption images with the Transformers Pipeline')

    # Directory, files, depth, saving method and config
    parser.add_argument('directory', type=str,
                        help='Directory to search for images')
    parser.add_argument('--depth', type=int, metavar='1',
                        help='Sets how deep to travel into folders, default is full, 1, 2, 3',
                        default=None)
    parser.add_argument('--mode', type=str,
                        choices=['write', 'append', 'prepend'],
                        default='write',
                        help='Sets the write mode to use when existing captions are found')
    parser.add_argument('--skip-existing', action='store_true',
                        help='Skip existing files if found')
    parser.add_argument('--ext', type=str, default='txt', metavar='txt or caption',
                        help='Extension for the caption files')
    parser.add_argument("--config", type=str, metavar="/path/to/config.ini", help="Use a configuration file")

    # Models, confidence, tokens, and other settings
    parser.add_argument('--model', type=str, choices=list(CAPTION_MODELS.keys()),
                        help='Model to use for captioning')
    parser.add_argument('--hf-override', type=str,
                        metavar='Mediocreatmybest/blip2-opt-2.7b-fp16-sharded or /file/path/',
                        help='Manually select either a Hugging Face model or file path')
    parser.add_argument('--clip-model', type=str, choices=list(ZEROSHOT_MODELS.keys()),
                        help='Model to use for CLIP/Zero Shot Category')
    parser.add_argument('--clip-cat', type=str, metavar='/path/textfile.txt',
                        help='File to CLIP/Zero Shot Category file')
    parser.add_argument('--clip-confidence', type=str, default=0.65, metavar='0.65', # set too high?
                        help='Categories with a score less than the set confidence level wont be included in final text output')
    parser.add_argument('--max-tokens', type=int, default=25, metavar='25', # max tokens for captions
                        help='The maximum number of tokens for the caption model')
    parser.add_argument('--min-tokens', type=int, default=8, metavar='8', # min tokens for captions, not available in pipeline
                        help='The minimum number of tokens for the caption model (Ignored with pipeline method)')
    parser.add_argument('--batch-count', default=1, type=int, metavar='2',
                        help='How many images to run in a batch, default is 1')
    parser.add_argument('--question', type=str,
                        metavar='Can you describe this image based on its art style and subject matter as concise as possible?',
                        help='Ask the model a question about the image. (Does not work with all models or that well really...)')

    # Model functions and methods
    parser.add_argument('--use-pipeline', action='store_true',
                        help='Use pipeline method for the caption model')
    parser.add_argument('--use-accelerate', action='store_true',
                        help='Use accelerate, this can help balance across GPU/vRAM/CPU/RAM (Not all models support this e.g. BLIP1)')
    parser.add_argument('--cpu-offload', action='store_true',
                        help='Switches to CPU only, can be slow but allows you to use RAM for larger models')
    parser.add_argument('--xbits', type=str, choices=['4bit', '8bit'], default=None,
                        help='Set 4 or 8 bit loading for captioning to help reduce vram usage (not supported in pipeline or cpu-offload)')

    # Other settings
    parser.add_argument('--quiet', action='store_true',
                        help='Supresses caption output')
    args = parser.parse_args()


    # Read the configuration file
    config = configparser.ConfigParser()

    # Check if a config file was provided before trying to read it
    if args.config is not None:
        config.read(args.config)
    # Use captioning section within the config file
    if config.has_section('captioning'):
        config_defaults = dict(config.items('captioning'))
    else:
        config_defaults = {}
    # Go through the config file and convert all values to the correct type
    args_defaults = {}
    for key, value in config_defaults.items():
        if value.isdigit():
            args_defaults[key] = int(value)
        else:
            args_defaults[key] = value

    # Merge the configuration file with the command line arguments
    # Hard to read, maybe move into separate variables?
    args = argparse.Namespace(**{**args_defaults, **vars(args)})

    # Exit if no model was selected
    if args.clip_model is None and args.model is None and args.hf_override is None:
        logging.info('No model was selected, exiting...')
        sys.exit()

    # Set device to cuda if available, else cpu or user sets cpu offload
    if args.cpu_offload:
        device = "cpu"
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    # Move args hf-override and model to caption_model
    if args.model:
        caption_model = CAPTION_MODELS[args.model]
    if args.hf_override:
        caption_model = args.hf_override

    # Convert confidence to a float
    confidence = float(args.clip_confidence)

    # Set the task to run
    model_task = "image-to-text"

    # Set configuration for pipeline / transformers
    config = CaptionConfig(model_id=caption_model,
                        quiet=args.quiet, task=model_task,
                        xbit=args.xbits, use_accelerate_auto=args.use_accelerate,
                        min_tokens=args.min_tokens, max_tokens=args.max_tokens, device=device)

    # Load models
    # Pipeline example from hugging face
    if args.model or args.hf_override:
        if args.use_pipeline and args.xbits:
            logging.info("4 or 8bit not available with pipeline, disabling xbits...")
            args.xbits = None

        # check if using pipeline method
        if args.use_pipeline:
            logging.info('Loading captioning task with pipeline...')

            # Now Set captioner from pipeline task function
            captioner = pipeline_task(config, model=config.model_id, use_fast=True)
        else:
            logging.info('Loading captioning model...')
            processor, model = load_caption_model(config)


    # Load CLIP zero shot if selected
    if args.clip_model:
        # Read the file and split it line by line
        logging.info('Loading zero-shot-image-classification task in pipeline...')
        zshot_cat = read_zshot(args.clip_cat)
        zshot = pipeline(task="zero-shot-image-classification",
                         model=ZEROSHOT_MODELS[args.clip_model], device=device, use_fast=True)

    # Use os walk plus to allow depth and file filtering
    for path, _, files in os_walk_plus(args.directory,
                                       file_filter=('.jpg', '.jpeg', '.png', '.webp'),
                                       max_depth=args.depth):

        # Batch processing logic, well. I guess I'd call this logic
        batches = [files[i:i+args.batch_count] for i in range(0, len(files), args.batch_count)]
        for batch in tqdm(batches, desc=f"Processing in batches of {args.batch_count}"):
            image_paths = [os.path.join(path, file) for file in batch]
            base_files = [splitext(image_path)[0] for image_path in image_paths]

            # Create captions and zshot_cats as empty lists
            captions = []
            zshot_cats = []

            # Use the list to store the images to that will be processed
            images_to_process = list(range(len(base_files)))  # by default, I'll process all images

            # Check for each image in the batch, if its text file exists
            if args.skip_existing:  # only check if args.skip_existing is selected
                images_to_process = []
                for i in range(len(base_files)):
                    # If text file doesnt exist for the image, add its index to images_to_process
                    if not does_file_exist(f"{base_files[i]}.{args.ext}"):
                        images_to_process.append(i)

            # Continue if there are any images to process
            if images_to_process:
                # Add the caption if selected
                # check if using pipeline
                if args.use_pipeline:
                    if args.model or args.hf_override:
                        captions = pipeline_caption_batch(captioner,
                                                          [image_paths[i] for i in images_to_process])
                else:
                    if args.model or args.hf_override:
                        captions = caption_generate(config,
                                                    images=[image_paths[i] for i in images_to_process],
                                                    processor=processor,
                                                    model=model, prompt_question=args.question)

                # Add zero-shot classifications if selected
                if args.clip_model:
                    zshot_cats = zshot_images_batch(zshot,
                                                    [image_paths[i] for i in images_to_process],
                                                    candidate_labels=zshot_cat,
                                                    confidence=confidence, quiet=args.quiet)

                # Combine captions and categories for each image
                for i, idx in enumerate(images_to_process):
                    # Start with empty caption
                    final_caption = []

                    # Add the caption if it's available and created
                    if i < len(captions):
                        final_caption.append(captions[i])

                    # Add the zshot categories if available
                    if i < len(zshot_cats):
                        final_caption.extend(zshot_cats[i])

                    # Use the full path to text file to save
                    full_path = f"{base_files[idx]}.{args.ext}"

                    # Save the final caption for each text file. No batching within text save
                    save_file(full_path, data=', '.join(final_caption), mode=args.mode)


if __name__ == "__main__":
    main()
