import os
from advanced_base64 import process_files, load_config

# Function to rename the file in place
def rename_file_in_place(original_path, new_filename):
    directory = os.path.dirname(original_path)
    extension = os.path.splitext(original_path)[1]
    new_path = os.path.join(directory, f"{new_filename}{extension}")
    
    try:
        os.rename(original_path, new_path)
        print(f"File renamed to: {new_path}")
    except OSError as e:
        print(f"Error renaming file: {e}")

# Main function to load config, process files, and rename them
def main():
    config = load_config()
    api_key = config['openai_api_key']
    
    # Specify either a single file or a directory of files
    path = "test_images/test_image.png"  # Change to a single file path or a directory path as needed
    
    # Process files and get the results
    results = process_files(path, api_key)
    
    # Rename the files based on the generated filenames
    for original_path, new_filename in results:
        rename_file_in_place(original_path, new_filename)

if __name__ == "__main__":
    main()