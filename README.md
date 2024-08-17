# Smart Screenshots

<p align="center">
  <img src="resources/icon.png" alt="Smart File Renamer" width="150">
</p>

# Smart File Renamer

![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg) ![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg) ![OpenAI API](https://img.shields.io/badge/OpenAI-API-orange.svg) ![Cloudinary Integration](https://img.shields.io/badge/Cloudinary-Integration-blueviolet.svg) ![Base64 Encoding](https://img.shields.io/badge/Base64-Encoding-brightgreen.svg) ![Pytesseract](https://img.shields.io/badge/Pytesseract-Text%20Extraction-lightgrey.svg) ![Transformers](https://img.shields.io/badge/Transformers-NLP-blue.svg)

## 🌟 Features

### 1. 🚀 Basic Method
- **Free and Generic Renaming**: This method provides basic renaming functionality without the need for any external APIs.
- **Ideal for**: Users who need simple file renaming based on content without any additional cost.

### 2. 🛠️ Advanced Method 1: Base64 Encoding with OpenAI API
- **Base64 Encoding**: This method encodes file content using Base64 and sends it to OpenAI's API for smart renaming.
- **Utilizes**: OpenAI API for intelligent and context-aware renaming.
- **Ideal for**: Users who require advanced renaming capabilities with an emphasis on privacy, using local encoding before processing.

### 3. ☁️ Advanced Method 2: Cloudinary Integration with OpenAI API
- **Cloudinary Integration**: This method uploads files to Cloudinary and then uses OpenAI’s API to analyze and rename files based on their content.
- **Utilizes**: Cloudinary for image management and OpenAI API for content analysis.
- **Ideal for**: Users who manage large media libraries and require cloud-based storage and processing.

## 🛤️ Roadmap

The Smart Screenshots project is continuously evolving. Here's what's in the pipeline:

- **📂 Other Format Support**: Expanding support to include additional file formats such as PDFs, videos, and more.
- **📏 Larger Image Size Support**: Improving the system to handle and process larger image files efficiently.
- **🖥️ Mac App (In Progress)**: Developing a native Mac application for a more seamless and integrated experience.

## 🛠️ Installation

To get started with Smart File Renamer, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pranav-Karra-3301/smart-screenshots.git
   cd smart-screenshots
   ```
   
2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Basic:
- **Install Tesseract OCR**:
    - **macOS**: 
      ```bash
      brew install tesseract
      ```
    - **Ubuntu**: 
      ```bash
      sudo apt-get install tesseract-ocr
      ```
    - **Windows**: Download from the [official site](https://github.com/tesseract-ocr/tesseract/wiki).

-  **Download the spaCy model**:
    ```bash
    python -m spacy download en_core_web_sm
    ```
### Advanced

- **Set Up Configuration**:
   - Create a `config.json` file in the root directory with the following keys:
   ```json
   {
     "openai_api_key": "your-openai-api-key",
     "cloudinary_cloud_name": "your-cloudinary-cloud-name",
     "cloudinary_api_key": "your-cloudinary-api-key",
     "cloudinary_api_secret": "your-cloudinary-api-secret"
   }
   ```




## 🚀 Usage

Follow the steps below to use each method:

### 1. Basic Method
- **Dependencies**: None required beyond basic Python packages.
- **Command**:
  ```bash
  python basic.py --input_folder <path-to-folder>
  ```

### 2. Advanced Method 1: Base64 Encoding with OpenAI API
- **Dependencies**: Requires OpenAI API key.
- **Command**:
    ```bash
    python rename_files_base64.py --input_folder <path-to-folder> --config config.json
    ```

### 3. Advanced Method 2: Cloudinary Integration with OpenAI API
- **Dependencies**: Requires both OpenAI API key and Cloudinary credentials.
- **Command**:
    ```bash
    python rename_files_cloudinary.py --input_folder <path-to-folder> --config config.json
    ```



## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Enjoy smart file renaming with advanced content recognition! 🎉

## 🙌 Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Pranav-Karra-3301/smart-screenshot-renamer/issues) for open issues or to start a discussion.

## 📞 Support

For any inquiries, suggestions, or issues, please [open an issue](https://github.com/Pranav-Karra-3301/smart-screenshot-renamer/issues) or contact me directly.
