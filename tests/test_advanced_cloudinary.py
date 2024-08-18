import unittest
from unittest.mock import patch, MagicMock
from owly.advanced_cloudinary import upload_image_to_cloudinary, initialize_cloudinary

class TestAdvancedCloudinary(unittest.TestCase):

    @patch('owly.advanced_cloudinary.cloudinary.uploader.upload')
    def test_upload_image_to_cloudinary(self, mock_upload):
        mock_upload.return_value = {"url": "http://example.com/uploaded_image.png"}
        image_url = upload_image_to_cloudinary("test_image.png")
        self.assertEqual(image_url, "http://example.com/uploaded_image.png")

    @patch('owly.advanced_cloudinary.cloudinary.config')
    def test_initialize_cloudinary(self, mock_config):
        config_data = {
            "cloud_name": "test_cloud_name",
            "api_key": "test_api_key",
            "api_secret": "test_api_secret"
        }
        initialize_cloudinary(config_data)
        mock_config.assert_called_with(
            cloud_name="test_cloud_name",
            api_key="test_api_key",
            api_secret="test_api_secret"
        )

if __name__ == "__main__":
    unittest.main()