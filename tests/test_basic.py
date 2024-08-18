import unittest
from owly.basic import extract_text_from_image, generate_caption, generate_smart_filename, rename_screenshot
from unittest.mock import patch, MagicMock

class TestBasic(unittest.TestCase):
    
    @patch('owly.basic.pytesseract.image_to_string')
    def test_extract_text_from_image(self, mock_ocr):
        mock_ocr.return_value = "This is a test text"
        text = extract_text_from_image("test_image.png")
        self.assertEqual(text, "This is a test text")
    
    @patch('owly.basic.BlipForConditionalGeneration.generate')
    @patch('owly.basic.BlipProcessor.decode')
    @patch('owly.basic.Image.open')
    def test_generate_caption(self, mock_open, mock_decode, mock_generate):
        mock_generate.return_value = ["caption tokenized output"]
        mock_decode.return_value = "Generated Caption"
        caption = generate_caption("test_image.png")
        self.assertEqual(caption, "Generated Caption")

    def test_generate_smart_filename(self):
        text = "John Doe visited New York on 2023-01-01"
        caption = "A person walking in the city"
        filename = generate_smart_filename(text, caption)
        self.assertEqual(filename, "John_Doe_New_York_2023-01-01")

    @patch('owly.basic.extract_text_from_image')
    @patch('owly.basic.generate_caption')
    @patch('os.rename')
    def test_rename_screenshot(self, mock_rename, mock_generate_caption, mock_extract_text):
        mock_extract_text.return_value = "Sample text"
        mock_generate_caption.return_value = "Sample caption"
        mock_rename.return_value = None

        rename_screenshot("test_screenshot.png")

        mock_rename.assert_called_once_with(
            "test_images/test_image.png"
        )

if __name__ == "__main__":
    unittest.main()