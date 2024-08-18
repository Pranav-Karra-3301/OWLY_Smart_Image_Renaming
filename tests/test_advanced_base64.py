import unittest
from unittest.mock import patch, mock_open, MagicMock
from owly_main.advanced_base64 import encode_image, generate_smart_filename, process_files

class TestAdvancedBase64(unittest.TestCase):

    def test_encode_image(self):
        with patch("builtins.open", mock_open(read_data=b"test image data")) as mock_file:
            encoded_image = encode_image("test_image.png")
            self.assertEqual(encoded_image, "dGVzdCBpbWFnZSBkYXRh")

    @patch('owly.advanced_base64.requests.post')
    def test_generate_smart_filename(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "Generated_Filename.png"}}]
        }

        base64_image = "dGVzdCBpbWFnZSBkYXRh"
        original_filename = "test_image.png"
        api_key = "fake-api-key"

        filename = generate_smart_filename(base64_image, original_filename, api_key)
        self.assertEqual(filename, "Generated_Filename.png")

    @patch('owly.advanced_base64.upload_image_to_cloudinary')
    @patch('owly.advanced_base64.generate_smart_filename')
    def test_process_files(self, mock_generate_smart_filename, mock_upload_image_to_cloudinary):
        mock_generate_smart_filename.return_value = "new_filename.png"
        mock_upload_image_to_cloudinary.return_value = "http://example.com/image.png"

        # Test with a single file
        with patch('os.path.isfile', return_value=True), patch('os.path.isdir', return_value=False):
            results = process_files("test_image.png", "fake-api-key")
            self.assertEqual(results, [("test_image.png", "new_filename.png")])

        # Test with a directory
        with patch('os.path.isfile', side_effect=[False, True]), patch('os.path.isdir', return_value=True), \
             patch('os.listdir', return_value=['file1.png']):
            results = process_files("test_directory", "fake-api-key")
            self.assertEqual(results, [("test_directory/file1.png", "new_filename.png")])

if __name__ == "__main__":
    unittest.main()