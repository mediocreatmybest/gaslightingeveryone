from dataclasses import dataclass

import requests
import torch
from PIL import Image
from transformers import AutoProcessor, Blip2ForConditionalGeneration, pipeline

TASKS = ["image-to-text", "zero-shot-image-classification", "visual-question-answering"]  # Limit inital tasks

# Create config class to pass to loading functions
from dataclasses import dataclass

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
    model_id: str = None
    pipeline: bool = True
    quiet: bool = False
    task: str = None
    min_tokens: int = 8
    max_tokens: int = 30
    xbit: str = None
    repetition_penalty: float = None
    use_accelerate_auto: bool = False
    kwargs: dict = None


def pipeline_task(task, model, use_accelerate_auto=False, device=0, quiet=False, **kwargs):
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
        print(f'Loading {task} and {model} in pipeline...')
        print('Total CUDA devices available:', torch.cuda.device_count())

    #for name, value in locals().items():
    #    if not name.startswith('__') and not callable(value):
    #        print(f"{name}: {value}")

    return pipeline_task


def load_caption_model(config: CaptionConfig, device):
    """ Load the caption model and processor.

    Args:
        config: An instance of the CaptionConfig class.
        device: Cuda device or CPU.

    Returns:
        processor and model from AutoProcessor and Blip2ForConditionalGeneration.
    """
    # TODO Add more models than just Blip2
    # Dictionary of args to pass to processor and model
    processor_args = {}
    model_args = {}

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

    processor = AutoProcessor.from_pretrained(config.model_id, **processor_args)
    model = Blip2ForConditionalGeneration.from_pretrained(config.model_id, **model_args)

    if not config.quiet:
        print(f'Loading {config.model_id}...')
        print(f'Using device: {device_map if config.use_accelerate_auto else {device}}')
        print('Total CUDA devices available:', torch.cuda.device_count())

    return processor, model


def caption_generate(config: CaptionConfig, images, processor, model, device, prompt_question=None):

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
    #prompt_question = "Question: how many cats are there? Answer:"

    # Check if we are using 4 or 8bit else default
    if config.xbit:
        inputs = processor(images=imagelist, text=prompt_question, return_tensors="pt").to(device, torch.float16)
    else:
        inputs = processor(images=imagelist, text=prompt_question, return_tensors="pt").to(device)

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
        if quiet is True:
            pass
        else:
            print('File: ', image_paths[i])
            print('Caption: ', stripped_caption)
        result.append(stripped_caption)
    return result

### testing
#device = "cuda" if torch.cuda.is_available() else "cpu"

#config = CaptionConfig(model_id="Mediocreatmybest/blip2-opt-2.7b_8bit",
#                       pipeline=False, quiet=False,
#                       xbit="4bit", use_accelerate_auto=True,
#                       min_tokens=8, max_tokens=30,)


# load model
#print("loading model...")
#processor, model = load_caption_model(config, device)

#print("next step...")

#url = "http://images.cocodataset.org/val2017/000000039769.jpg"
#url1 = "http://images.cocodataset.org/val2017/000000039769.jpg"
#image0 = Image.open(requests.get(url, stream=True).raw)
#image1 = Image.open(requests.get(url, stream=True).raw)
#image0 = "C:\\xyz\\xyz.png"
#image1 = "C:\\xyz\\xyz.png"
#batch = [image0, image1]


# generate caption
#print("generating caption...")
#caption = caption_generate(config, images=batch, processor=processor, model=model, device=device)

#print(caption)