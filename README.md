# 📸 Smart Screenshot Renamer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 🚀 Overview

**Smart Screenshot Renamer** is a powerful Python script designed to intelligently rename your screenshots. By leveraging state-of-the-art OCR, NLP, and image captioning techniques, this tool automatically generates meaningful filenames for your screenshots. Whether it's recognizing text, identifying objects, or even capturing the essence of a scene, Smart Screenshot Renamer ensures your files are organized with relevant, easy-to-understand names.

## 🛠️ Features

- **OCR Integration**: Extracts text from images using Tesseract.
- **Image Captioning**: Uses the BLIP model to generate captions based on image content.
- **NLP-Powered Filename Generation**: Utilizes spaCy to analyze extracted text and generate contextually appropriate filenames.
- **Batch Processing**: Automatically processes and renames all screenshots in a specified directory.
- **Cross-Platform**: Works seamlessly on any system with Python installed.

## 🧰 Requirements

- **Python 3.8+**
- **pytesseract**: Tesseract OCR wrapper for Python.
- **Pillow**: Python Imaging Library to handle image processing.
- **spaCy**: Industrial-strength NLP in Python.
- **PyTorch**: Deep learning framework for BLIP model.
- **Transformers**: Hugging Face's library for state-of-the-art NLP.

### 📦 Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Pranav-Karra-3301/smart-screenshot-renamer.git
    cd smart-screenshot-renamer
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Tesseract OCR**:
    - **macOS**: 
      ```bash
      brew install tesseract
      ```
    - **Ubuntu**: 
      ```bash
      sudo apt-get install tesseract-ocr
      ```
    - **Windows**: Download from the [official site](https://github.com/tesseract-ocr/tesseract/wiki).

4. **Download the spaCy model**:
    ```bash
    python -m spacy download en_core_web_sm
    ```

## 🚀 Usage

1. **Configure the directory**: Replace the path in `screenshots_directory` with the path to your screenshots folder.

2. **Run the script**:
    ```bash
    python rename_screenshots.py
    ```

3. **Watch the magic happen**: The script will process each screenshot, generate a smart filename, and rename the file accordingly.

## ⚙️ How It Works

1. **OCR Extraction**: The script extracts any text present in the image using Tesseract OCR.
2. **Image Captioning**: The BLIP model generates a caption that describes the image.
3. **NLP Processing**: Extracts entities like names, dates, and locations from the text.
4. **Smart Filename Generation**: Combines the extracted text, recognized entities, and image caption to create a meaningful filename.
5. **Batch Processing**: All screenshots in the specified directory are processed in one go.

## 🛡️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🙌 Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Pranav-Karra-3301/smart-screenshot-renamer/issues) for open issues or to start a discussion.

## 📞 Support

For any inquiries, suggestions, or issues, please [open an issue](https://github.com/Pranav-Karra-3301/smart-screenshot-renamer/issues) or contact me directly.