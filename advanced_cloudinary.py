import cloudinary
import cloudinary.uploader
import requests
import os
import json

# Load the configuration from the config.json file
def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

# Initialize Cloudinary with API keys
def initialize_cloudinary(config):
    cloudinary.config(
        cloud_name=config['cloudinary_cloud_name'],
        api_key=config['cloudinary_api_key'],
        api_secret=config['cloudinary_api_secret']
    )

# Upload the image to Cloudinary and retrieve the URL
def upload_image_to_cloudinary(file_path):
    response = cloudinary.uploader.upload(file_path)
    image_url = response['secure_url']
    print(f"Uploaded Image URL: {image_url}")
    return image_url

# Generate a smart filename using the ChatCompletion API with the Cloudinary URL
def generate_smart_filename(image_url, original_filename, api_key):
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
                            "url": image_url
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
        image_url = upload_image_to_cloudinary(path)
        new_filename = generate_smart_filename(image_url, os.path.basename(path), api_key)
        if new_filename:
            results.append((path, new_filename))
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                image_url = upload_image_to_cloudinary(file_path)
                new_filename = generate_smart_filename(image_url, filename, api_key)
                if new_filename:
                    results.append((file_path, new_filename))
    else:
        print(f"{path} is neither a file nor a directory.")
    return results

# Main function to load config and process files (can be run separately for testing)
def main():
    config = load_config()
    api_key = config['openai_api_key']
    initialize_cloudinary(config)
    
    # Specify either a single file or a directory of files
    path = "files/"  # Change to a single file path or a directory path as needed
    
    results = process_files(path, api_key)
    print("Processing complete. Results:", results)

if __name__ == "__main__":
    main()