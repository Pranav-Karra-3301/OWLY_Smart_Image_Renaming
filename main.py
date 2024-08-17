import os
import pytesseract
from PIL import Image
import spacy
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load spaCy's English model
nlp = spacy.load('en_core_web_sm')

# Load BLIP model for image captioning
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

def extract_text_from_image(image_path):
    """Extract text from image using Tesseract OCR"""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def generate_caption(image_path):
    """Generate a caption for the image using BLIP"""
    raw_image = Image.open(image_path).convert("RGB")
    inputs = processor(raw_image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def generate_smart_filename(text, caption):
    """Generate a smart filename based on context using NLP and image captioning"""
    doc = nlp(text)
    
    # Extract relevant entities and keywords
    entities = [ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'EVENT']]
    
    if entities:
        filename = "_".join(entities[:3])
    elif caption:
        filename = caption.replace(" ", "_")
    else:
        filename = "screenshot"
    
    return filename

def rename_screenshot(screenshot_path):
    """Perform OCR, image captioning, generate a new name, and rename the screenshot"""
    text = extract_text_from_image(screenshot_path)
    caption = generate_caption(screenshot_path)
    
    new_name = generate_smart_filename(text, caption)
    
    if new_name:
        directory, _ = os.path.split(screenshot_path)
        new_file_path = os.path.join(directory, f"{new_name}.png")
        os.rename(screenshot_path, new_file_path)
        print(f"Renamed to: {new_file_path}")
    else:
        print("Could not generate a meaningful name.")

def process_screenshots_in_directory(directory):
    """Process and rename all screenshots in the specified directory"""
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            screenshot_path = os.path.join(directory, filename)
            rename_screenshot(screenshot_path)

# Replace with the path of your screenshots folder
screenshots_directory = '/Users/pranavkarra/Desktop/Screenshots'
process_screenshots_in_directory(screenshots_directory)