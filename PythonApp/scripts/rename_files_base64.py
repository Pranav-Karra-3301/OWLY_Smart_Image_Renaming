import os
import sys
from scripts.advanced_base64 import process_files, load_config
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal
from index_manager import IndexManager

class FileProcessor(QObject):
    progress_update = pyqtSignal(int, int)
    process_complete = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.index_manager = IndexManager()

    def rename_file_in_place(self, original_path, new_filename):
        directory = os.path.dirname(original_path)
        extension = os.path.splitext(original_path)[1]
        new_filename = new_filename.strip('"').rstrip(extension)  
        new_path = os.path.join(directory, f"{new_filename}{extension}")
        
        try:
            os.rename(original_path, new_path)
            print(f"File renamed to: {new_path}")
            return new_path
        except OSError as e:
            print(f"Error renaming file: {e}")
            return None

    def process_and_rename(self, path):
        config = load_config()
        api_key = config['openai_api_key']
        
        files_to_process = []
        if os.path.isfile(path):
            files_to_process.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    files_to_process.append(os.path.join(root, file))

        total_files = len(files_to_process)
        processed_files = 0

        for index, file_path in enumerate(files_to_process, 1):
            if self.index_manager.is_file_processed(file_path):
                print(f"Skipping already processed file: {file_path}")
                continue

            results = process_files(file_path, api_key)
            for original_path, new_filename, description in results:
                new_path = self.rename_file_in_place(original_path, new_filename)
                if new_path:
                    self.index_manager.add_processed_file(original_path, new_path, new_filename, description)
                    processed_files += 1
            
            self.progress_update.emit(index, total_files)

        message = f"Processed {processed_files} out of {total_files} files in: {path}"
        self.process_complete.emit(message)

def main():
    app = QApplication(sys.argv)
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "test_images/test_image.png"  

    processor = FileProcessor()
    processor.process_and_rename(path)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()