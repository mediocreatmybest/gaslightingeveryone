""" Set logging level with logging"""
import logging
from dataclasses import dataclass

from typing import Optional


import torch
from PIL import Image
from transformers import (AutoModelForCausalLM, AutoProcessor,
                          Blip2ForConditionalGeneration,
                          BlipForConditionalGeneration, pipeline)
# Set our loggins level to INFO
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TASKS = ["image-to-text", "zero-shot-image-classification", "visual-question-answering"]  # Limit inital tasks



@dataclass
class CaptionConfig:
    """ Configuration for Transformers and Transformers Pipeline.

    Args:
        model_id (str): The model id of the model e.g. "Mediocreatmybest/blip2-opt-2.7b_8bit"
        pipeline (bool): If True use pipeline API, otherwise we don't
        quiet (bool): Suppress some of the console output
        task (str): The task to perform if pipeline API is used (e.g. "image-to-text")
        max_tokens (int): The maximum number of tokens to generate.
        min_tokens (int): The minimum number of tokens to generate, ignored with pipeline API.
        xbit (str): The number of bits to use for quantization (e.g. "8bit"), otherwise None.
        repetition_penalty (float): The repetition penalty to use. (can be moved to kwargs)
        use_accelerate_auto (bool): Use accelerate "auto" to balance model across devices.
        **kwargs: Additional keyword arguments to pass along.
        TODO: remove duplicate args
    """
    model_id: str
    xbit: Optional[str] = None
    repetition_penalty: Optional[float] = None
    kwargs: Optional[dict] = None
    device: str = None
    pipeline: bool = True
    quiet: bool = False
    task: str = "image-to-text"
    min_tokens: int = 8
    max_tokens: int = 30
    use_accelerate_auto: bool = False

    def __post_init__(self):
    # Setting here the default device to allow us to override it with the config
        if self.device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

def pipeline_task(task, model, use_accelerate_auto=False, device=CaptionConfig.device, quiet=False, **kwargs):
    """
    Load a simple task sequence with model using the Transformers pipeline.

    task: the pipeline task to use (e.g., 'image-to-text')
    model: HuggingFace model to load (e.g. Mediocreatmybest/blip2-opt-2.7b-fp16-sharded)
    use_accelerate: whether to use the accelerate library for device_map (e.g. True/False)
    device: int or str, the device to use for processing.
                   If use_accelerate is True, this will switch to device_map="auto"
    kwargs: any other pipeline parameter
    return: the pipe
    TODO: use config class to remove some of the kwargs
    """
    if task not in TASKS:
        raise ValueError(f"Invalid task: {task}")

    if use_accelerate_auto:
        # Switch device to auto unless cpu is forced
        device = "auto" if use_accelerate_auto and device != "cpu" else device

        # Now Set captioner function
        #model_kwargs={f"load_in_8bit": True, "torch_dtype": torch.float16} # leaving until I can work this out
        pipeline_task = pipeline(task=task, model=model, device_map=device, **kwargs)

    # loading without Accelerate device mapping
    else:
        pipeline_task = pipeline(task=task, model=model, device=device, **kwargs)

    if quiet is False:
        logging.info('Loading %s and %s in pipeline...', task, model)
        logging.info('Total CUDA devices available: %d', torch.cuda.device_count())

    return pipeline_task


def load_caption_model(config: CaptionConfig):
    """ Load the caption model and processor.

    Args:
        config: An instance of the CaptionConfig.

    Returns:
        processor and model from AutoProcessor and Blip2ForConditionalGeneration.
    """
    # Dictionary of args to pass to processor and model
    processor_args = {}
    model_args = {}

    # Configure settings
    if config.xbit == "8bit":
        processor_args["load_in_8bit"] = True
        model_args["load_in_8bit"] = True
    elif config.xbit == "4bit":
        processor_args["load_in_4bit"] = True
        model_args["load_in_4bit"] = True

    if config.repetition_penalty:
        model_args["repetition_penalty"] = config.repetition_penalty

    if config.use_accelerate_auto:
        device_map = "auto"
        processor_args["device_map"] = device_map
        model_args["device_map"] = device_map

    # Model check to see which model to load
    model_check = config.model_id.split("/")

    # Load BLIP 2 model and processor
    if model_check[1].startswith("blip2-"):
        processor = AutoProcessor.from_pretrained(config.model_id, **processor_args)
        model = Blip2ForConditionalGeneration.from_pretrained(config.model_id, **model_args)
        if not config.quiet:
            logging.info("Loading BLIP2 model")

    # Load BLIP model and processor
    elif model_check[1].startswith("blip-"):
        processor = AutoProcessor.from_pretrained(config.model_id, **processor_args)
        model = BlipForConditionalGeneration.from_pretrained(config.model_id, **model_args)
        if not config.quiet:
            logging.info("Loading BLIP model")

    elif model_check[1].startswith("git-"):
        processor = AutoProcessor.from_pretrained(config.model_id, **processor_args)
        model = AutoModelForCausalLM.from_pretrained(config.model_id, **model_args)
        if not config.quiet:
            logging.info("Loading Git model")

    else:
        processor = AutoProcessor.from_pretrained(config.model_id, **processor_args)
        model = AutoModelForCausalLM.from_pretrained(config.model_id, **model_args)
        if not config.quiet:
            logging.info("Loading with AutoModel...")

    # xbit doesn't support .to(device)
    # If xbit or accelerate is not set, move to device for all models
    if not config.xbit and config.use_accelerate_auto is False:
        model = model.to(config.device)

    if not config.quiet:
        logging.info('Loading %s...', config.model_id)
        logging.info('Using device: %s', device_map if config.use_accelerate_auto else config.device)
        logging.info('Total CUDA devices available: %d', torch.cuda.device_count())

    return processor, model


def caption_generate(config: CaptionConfig, images, processor, model, prompt_question=None):

    # Collect config
    if config.repetition_penalty:
        repetition_penalty = config.repetition_penalty
    else:
        repetition_penalty = None
    if config.min_tokens:
        min_tokens = config.min_tokens
    if config.max_tokens:
        max_tokens = config.max_tokens

    # convert PIL image and append to list
    imagelist = []
    for img in images:
        img = Image.open(img)
        imagelist.append(img)

    # min_new_tokens will affect the output length even with prompt_question
    # prompt_question = "Question: how many cats are there? Answer:"

    # Check if we are using 4 or 8bit else default
    if config.xbit:
        inputs = processor(images=imagelist, text=prompt_question,
                           return_tensors="pt").to(config.device, torch.float16) # pylint: disable=no-member
    else:
        inputs = processor(images=imagelist, text=prompt_question,
                           return_tensors="pt").to(config.device)


    generated_ids = model.generate(**inputs, repetition_penalty=repetition_penalty,
                                   min_new_tokens=min_tokens,
                                   max_new_tokens=max_tokens)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)

    return generated_text


# Batch caption attempt need to make more generic captions option
def pipeline_caption_batch(captioner, image_paths, quiet=False):
    captions = captioner(image_paths)
    result = []
    for i, caption in enumerate(captions):
        stripped_caption = str(caption[0]['generated_text']).strip()

        if not quiet:
            logging.info('File: %s', image_paths[i])
            logging.info('Caption: %s', stripped_caption)


        result.append(stripped_caption)
    return result
