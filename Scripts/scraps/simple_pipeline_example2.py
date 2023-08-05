from func_transformers import CaptionConfig, pipeline_caption_batch, pipeline_task

# Set configuration for pipeline / transformers
config = CaptionConfig(
    model_id="Salesforce/blip-image-captioning-base"
    )

# Load the captioner pipeline with config
captioner = pipeline_task(
                        config,
                        model=config.model_id,
                        use_fast=True,
                        generate_kwargs={"min_new_tokens": 8, "max_new_tokens": 30},
                        model_kwargs={"load_in_4bit": True})

# Create output from captioner batch function
output = pipeline_caption_batch(captioner=captioner,
                                #URL or Path to image
                                image_paths=["https://huggingface.co/datasets/Narsil/image_dummy/raw/main/lena.png"]
                                )

print(output)