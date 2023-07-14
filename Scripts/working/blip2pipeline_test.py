from transformers import pipeline
import torch


image = "https://huggingface.co/datasets/Narsil/image_dummy/raw/main/parrots.png"
#model = "Mediocreatmybest/blip2-opt-2.7b-fp16-sharded"
model = "Mediocreatmybest/blip2-opt-2.7b_8bit"

#model_kwargs = {"load_in_8bit": False, "torch_dtype": torch.float16}
captioner = pipeline(task="image-to-text",
                            model=model,
                            max_new_tokens=30,
                            device_map="auto", model_kwargs=None, use_fast=True
                            )
# load model
#captioner.model.to(torch.float16)
captioner
# caption
caption = captioner(image)[0]['generated_text']
print(caption)