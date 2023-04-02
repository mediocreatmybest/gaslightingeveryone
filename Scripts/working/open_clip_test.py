# https://github.com/mlfoundations/open_clip
# example code
import torch
from PIL import Image
import open_clip

model, _, preprocess = open_clip.create_model_and_transforms('ViT-H-14', pretrained='laion2b_s32b_b79k')
tokenizer = open_clip.get_tokenizer('ViT-H-14')

image = preprocess(Image.open("test.png")).unsqueeze(0)

with open('medium.txt', 'r', encoding='utf-8') as f:
    mediumtoken = []
    for lines in f:
        mediumtoken.append(lines)

text = tokenizer(mediumtoken)

with torch.no_grad(), torch.cuda.amp.autocast():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)

for i, medium in enumerate(mediumtoken):
    score = text_probs[0][i].item() * 100
    print(f"{medium.strip()}: {score:.2f}%")
