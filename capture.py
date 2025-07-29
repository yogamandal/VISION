import cv2
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Capture image from webcam
cap = cv2.VideoCapture(0)  # 0 = default MacBook webcam
if not cap.isOpened():
    raise Exception("Could not open webcam")

print("📸 Capturing image... Look at the camera.")
ret, frame = cap.read()
cap.release()

if not ret:
    raise Exception("Failed to capture image")

# Convert frame to PIL image
image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# Generate scene description using BLIP
print("🧠 Generating scene description...")
inputs = processor(images=image, return_tensors="pt")
out = model.generate(**inputs)
caption = processor.decode(out[0], skip_special_tokens=True)

print("📝 Scene Description:", caption)
