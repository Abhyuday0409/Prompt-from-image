import open_clip
import torch
from PIL import Image

def generate_prompt_from_image(image_path):
    model, _, transform = open_clip.create_model_and_transforms(
        model_name="coca_ViT-L-14",
        pretrained="mscoco_finetuned_laion2B-s13B-b90k"
    )
    
    im = Image.open(image_path).convert("RGB")
    im = transform(im).unsqueeze(0)
    
    with torch.no_grad(), torch.cuda.amp.autocast():
        generated = model.generate(im)
    
    prompt = open_clip.decode(generated[0]).split("<end_of_text>")[0].replace("<start_of_text>", "")
    
    return prompt
