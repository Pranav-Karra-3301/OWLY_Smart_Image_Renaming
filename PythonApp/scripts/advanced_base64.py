import base64
import os
import json
import requests

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_smart_filename(base64_image, original_filename, api_key):
    if requests is None:
        print("Cannot generate smart filename: 'requests' module is not available")
        return None, None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    system_prompt = (
        "You are an AI trained to generate concise, context-aware filenames and descriptions "
        "for images. When provided with an image, create a filename that accurately "
        "describes its content and a brief description that summarizes the image in one or two sentences. "
        "If the image features a scene from a movie, TV show, or a famous person, include the name of the TV show/Movie/Celebrity in the filename and description. Ensure the filename is not longer than 150 characters "
        "but captures the essence of the image or file."
        "If it has Math, make sure to include Math in the filename, and if possible even specifics like Calculus, Algebra, etc."
        "If it has code or programming, make sure to include Code in the filename, and if possible even specifics like Python, Java, etc."
        "If it has Chats, make sure to include Chat in the filename, and if possible even specifics like WhatsApp, Instagram, Discord, Slack, etc."
        "If it has a website, make sure to include Website in the filename, and if possible even specifics like Google, Facebook, etc."
        "If it has a graph, make sure to include Graph in the filename, and if possible even specifics like Bar Graph, Line Graph, etc."
        "Return the result in the following JSON format: {\"filename\": \"<generated_filename>\", \"description\": \"<brief_description>\"}."
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

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response_data = response.json()
        
        if "choices" in response_data and len(response_data["choices"]) > 0:
            result = response_data['choices'][0]['message']['content'].strip()
            result_json = json.loads(result)
            filename = result_json['filename']
            description = result_json['description']
            print(f"Generated Filename for {original_filename}: {filename}")
            print(f"Description: {description}")
            return filename, description
        else:
            print("Failed to generate filename and description.")
            print(response_data)  
            return None, None
    except requests.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        print(f"Response content: {response.text}")
        return None, None

def process_files(path, api_key):
    results = []
    if os.path.isfile(path):
        base64_image = encode_image(path)
        new_filename, description = generate_smart_filename(base64_image, os.path.basename(path), api_key)
        if new_filename:
            results.append((path, new_filename, description))
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                base64_image = encode_image(file_path)
                new_filename, description = generate_smart_filename(base64_image, filename, api_key)
                if new_filename:
                    results.append((file_path, new_filename, description))
    else:
        print(f"{path} is neither a file nor a directory.")
    return results

def main():
    config = load_config()
    api_key = config['openai_api_key']
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        return "Please provide a file or directory path as an argument."
    
    results = process_files(path, api_key)
    print("Processing complete. Results:", results)

if __name__ == "__main__":
    import sys
    main()