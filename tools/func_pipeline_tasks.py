import torch
from transformers import pipeline


TASKS = ["image-to-text", "zero-shot-image-classification"]  # Limit inital tasks


def pipeline_task(task, model, use_accelerate_auto=False, device=0, quiet=False, **kwargs):
    """
    Load simple task sequence with a model using the Transformers pipeline.

    task: the pipeline task to use (e.g., 'image-to-text')
    model: HuggingFace model to load (e.g. Mediocreatmybest/blip2-opt-2.7b-fp16-sharded)
    use_accelerate: whether to use the accelerate library for device_map (e.g. True/False)
    device: int or str, the device to use for processing.
                   If use_accelerate is True, this will switch to device_map="auto"
    kwargs: any other pipeline parameter
    return: the pipe
    """
    if task not in TASKS:
        raise ValueError(f"Invalid task: {task}")

    if use_accelerate_auto:
        # Switch device to auto unless cpu is forced
        if device == "cpu":
            device = "cpu"
        else:
            device = "auto"
        # Now Set captioner function
        pipeline_task = pipeline(task=task, model=model, device_map=device, **kwargs)
    # loading without Accelerate device mapping
    else:
        pipeline_task = pipeline(task=task, model=model, device=device, **kwargs)

    if quiet is False:
        print(f'Loading {task} and {model} in pipeline...')
        print('Total CUDA devices available:', torch.cuda.device_count())

    return pipeline_task