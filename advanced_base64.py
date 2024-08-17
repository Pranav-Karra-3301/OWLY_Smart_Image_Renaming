import base64
import requests
import os
import json

# Load the configuration from the config.json file
def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Generate a smart filename using the ChatCompletion API with the base64 image
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
        "model": "gpt-4o-mini",
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
    
    # Check if the response is successful
    if "choices" in response_data and len(response_data["choices"]) > 0:
        filename = response_data['choices'][0]['message']['content'].strip()
        print(f"Generated Filename for {original_filename}: {filename}")
        return filename
    else:
        print("Failed to generate filename.")
        print(response_data)  # Print the error details
        return None

# Function to process files (this function will be called by the renaming script)
def process_files(path, api_key):
    results = []
    if os.path.isfile(path):
        base64_image = encode_image(path)
        new_filename = generate_smart_filename(base64_image, os.path.basename(path), api_key)
        if new_filename:
            results.append((path, new_filename))
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                base64_image = encode_image(file_path)
                new_filename = generate_smart_filename(base64_image, filename, api_key)
                if new_filename:
                    results.append((file_path, new_filename))
    else:
        print(f"{path} is neither a file nor a directory.")
    return results

# Main function to load config and process files (can be run separately for testing)
def main():
    config = load_config()
    api_key = config['openai_api_key']
    
    # Specify either a single file or a directory of files
    path = "images/img.png"  # Change to a single file path or a directory path as needed
    
    results = process_files(path, api_key)
    print("Processing complete. Results:", results)

# if you want to test only process_files.py, run main(), and see the generated file names

if __name__ == "__main__":
    main()