from transformers import pipeline

pipe = pipeline("image-to-text",
                model="Salesforce/blip-image-captioning-base",
                generate_kwargs={"min_new_tokens": 8, "max_new_tokens": 30},
                model_kwargs={"load_in_4bit": True}
                )
caption = pipe("https://huggingface.co/datasets/Narsil/image_dummy/raw/main/parrots.png")

print(caption)