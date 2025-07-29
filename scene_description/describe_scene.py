from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def describe_image(image_path: str) -> str:
    try:
        # Load image using PIL
        image = Image.open(image_path).convert('RGB')
        
        # Preprocess image
        inputs = processor(images=image, return_tensors="pt")

        # Forward pass
        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokens=True)

        return description
    except Exception as e:
        print(f"❌ Error in describe_image(): {e}")
        return "Sorry, I couldn't understand the image."
