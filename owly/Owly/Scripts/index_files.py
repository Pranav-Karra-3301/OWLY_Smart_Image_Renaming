import os
import sys
import json
import requests
import base64
from PIL import Image
import pytesseract

def fetch_api_key():
    if len(sys.argv) < 3:
        print("API key is missing")
        sys.exit(1)
    return sys.argv[2]

def generate_tags_and_description(image_path, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    system_prompt = (
        "You are an AI trained to generate concise, context-aware metadata for images. "
        "When provided with an image, generate a description and a list of relevant tags. "
        "The description should be no longer than 60 words, and the tags should be separated by commas."
    )

    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    if "choices" in response_data and len(response_data["choices"]) > 0:
        content = response_data['choices'][0]['message']['content'].strip()
        parts = content.split(";")
        if len(parts) >= 2:
            description = parts[0].strip()
            tags = parts[1].strip()
            return tags, description
        else:
            return "", "Failed to parse tags and description"
    else:
        print("Failed to generate tags and description.")
        print(response_data)
        return "", "Error with OpenAI API"

def perform_ocr(file_path):
    try:
        text = pytesseract.image_to_string(Image.open(file_path))
        return text
    except Exception as e:
        print(f"Error performing OCR on {file_path}: {e}")
        return ""

def index_files(directory, api_key):
    file_index = []
    total_files = sum([len(files) for r, d, files in os.walk(directory) if any(f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) for f in files)])
    processed = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                
                tags, description = generate_tags_and_description(file_path, api_key)
                ocr_text = perform_ocr(file_path)
                timestamp = os.path.getmtime(file_path)

                file_index.append({
                    "path": file_path,
                    "name": file_name,
                    "tags": tags,
                    "description": description,
                    "ocr": ocr_text,
                    "timestamp": timestamp
                })

                processed += 1
                progress = processed / total_files
                print(f"PROGRESS:{progress:.2f}")
                print(f"UNPROCESSED:{total_files - processed}")
                sys.stdout.flush()

    print(json.dumps(file_index))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: index_files.py <directory> <api_key>")
        sys.exit(1)

    directory = sys.argv[1]
    api_key = fetch_api_key()
    index_files(directory, api_key)
