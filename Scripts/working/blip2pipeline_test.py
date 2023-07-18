import tokenize
from transformers import pipeline, AutoProcessor, AutoTokenizer
import torch


device = "cuda" if torch.cuda.is_available() else "cpu"


image = "https://huggingface.co/datasets/Narsil/image_dummy/raw/main/parrots.png"
#model = "Mediocreatmybest/blip2-opt-2.7b-fp16-sharded"
#model = "Mediocreatmybest/blip2-opt-2.7b_8bit"
model = "Salesforce/blip-image-captioning-large"

#model_kwargs = {"load_in_8bit": False, "torch_dtype": torch.float16}
captioner = pipeline(task="image-to-text",
                            model=model,
                            max_new_tokens=30,
                            model_kwargs=None, use_fast=False, device_map="auto"
                            )
# load model
#captioner.model.to(torch.float16)
captioner
# caption
caption = captioner(image)[0]['generated_text']
print(caption)