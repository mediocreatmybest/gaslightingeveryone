from transformers import pipeline

device = "cpu"

captioner = pipeline(task="image-to-text",
                     model="Salesforce/blip2-flan-t5-xl",
                     max_new_tokens=100,  # replace with your value
                     device=device, use_fast=True)

prompt = "Question: how many cats are there? Answer:"

# Path to image
image_path = "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&dl=alvan-nee-ZCHj_2lJP00-unsplash.jpg&w=640"

# Generate caption
result = captioner(image_path, prompt)

print(result)
