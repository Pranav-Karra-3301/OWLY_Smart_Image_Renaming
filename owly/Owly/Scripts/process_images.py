import base64
import requests
import os
import sys
import json

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_smart_filename(base64_image, original_filename, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    system_prompt = (
        "You are an AI trained to generate concise, context-aware filenames "
        "for images. When provided with an image, create a filename that accurately "
        "describes its content. If the image features a scene from a movie, TV show, "
        "or a famous person, include the name of the TV show/Movie/Celebrity in the filename. Ensure the filename is not longer than 150 characters. but be specific enough, "
        "but captures the essence of the image or file."
        "If it has Math, make sure to include Math in the filename, and if possible even specifics like Calculus, Algebra, etc."
        "If it has code or programming, make sure to include Code in the filename, and if possible even specifics like Python, Java, etc."
        "If it has Chats, make sure to include Chat in the filename, and if possible even specifics like whatsapp, instagram, Discord, Slack, etc."
        "If it has a website, make sure to include Website in the filename, and if possible even specifics like Google, Facebook, etc."
        "If it has a graph, make sure to include Graph in the filename, and if possible even specifics like Bar Graph, Line Graph, etc."
    )

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
                            "url": f"data:image/jpeg;base64,{base64_image}"
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
        filename = response_data['choices'][0]['message']['content'].strip()
        print(f"Generated Filename for {original_filename}: {filename}")
        return filename
    else:
        print("Failed to generate filename.")
        print(response_data)
        return None

def process_files(path, api_key):
    results = []
    total_files = 0
    processed = 0

    if os.path.isfile(path):
        total_files = 1
    elif os.path.isdir(path):
        total_files = sum([len(files) for r, d, files in os.walk(path) if any(f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) for f in files)])

    def process_single_file(file_path):
        nonlocal processed
        base64_image = encode_image(file_path)
        new_filename = generate_smart_filename(base64_image, os.path.basename(file_path), api_key)
        if new_filename:
            results.append((file_path, new_filename))
        processed += 1
        progress = processed / total_files
        print(f"PROGRESS:{progress:.2f}")
        print(f"UNPROCESSED:{total_files - processed}")
        sys.stdout.flush()

    if os.path.isfile(path):
        process_single_file(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    file_path = os.path.join(root, file)
                    process_single_file(file_path)
    else:
        print(f"{path} is neither a file nor a directory.")

    return results

def rename_file_in_place(original_path, new_filename):
    directory = os.path.dirname(original_path)
    extension = os.path.splitext(original_path)[1]
    new_path = os.path.join(directory, f"{new_filename}{extension}")
    
    try:
        os.rename(original_path, new_path)
        print(f"File renamed to: {new_path}")
    except OSError as e:
        print(f"Error renaming file: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: process_images.py <directory> <api_key>")
        sys.exit(1)

    path = sys.argv[1]
    api_key = sys.argv[2]
    
    results = process_files(path, api_key)
    
    for original_path, new_filename in results:
        rename_file_in_place(original_path, new_filename)

if __name__ == "__main__":
    main()
