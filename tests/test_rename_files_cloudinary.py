import unittest
from owly.rename_files_cloudinary import rename_file_in_place
from unittest.mock import patch, MagicMock

class TestRenameFilesCloudinary(unittest.TestCase):

    @patch('os.rename')
    def test_rename_file_in_place(self, mock_rename):
        mock_rename.return_value = None
        
        original_path = "path/to/file.png"
        new_filename = "new_file_name"
        
        rename_file_in_place(original_path, new_filename)
        
        mock_rename.assert_called_once_with(
            "path/to/file.png",
            "path/to/new_file_name.png"
        )

if __name__ == "__main__":
    unittest.main()