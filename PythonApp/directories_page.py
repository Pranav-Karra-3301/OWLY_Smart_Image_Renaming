import os
import subprocess
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QFileDialog, 
                             QMessageBox, QProgressBar, QLabel)
from PyQt6.QtCore import QThread, pyqtSignal, QSettings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from index_manager import IndexManager

class WorkerThread(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, files_to_process, progress_callback, index_manager):
        super().__init__()
        self.files_to_process = files_to_process
        self.progress_callback = progress_callback
        self.index_manager = index_manager

    def run(self):
        try:
            total_files = len(self.files_to_process)
            processed_files = 0
            
            for file_path in self.files_to_process:
                new_filename, description = self.process_file(file_path)
                if new_filename:
                    new_path = os.path.join(os.path.dirname(file_path), new_filename)
                    self.index_manager.add_processed_file(file_path, new_path, new_filename, description)
                processed_files += 1
                self.progress_callback(processed_files, total_files)
            
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the scripts: {e}")
        self.finished.emit()

    def process_file(self, file_path):
        try:
            result = subprocess.run(["python3", "scripts/advanced_base64.py", file_path], check=True, capture_output=True, text=True)
            filename_and_description = result.stdout.strip().split('|')
            if len(filename_and_description) == 2:
                new_filename = filename_and_description[0].strip()
                description = filename_and_description[1].strip()

                rename_result = subprocess.run(["python3", "scripts/rename_files_base64.py", file_path, new_filename], check=True)
                if rename_result.returncode == 0:
                    return new_filename, description
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while processing {file_path}: {e}")
        return None, None

class FileHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        if not event.is_directory:
            self.callback(event.src_path)

class DirectoriesPage(QWidget):
    process_directory_signal = pyqtSignal(str)

    def __init__(self, index_manager):
        super().__init__()
        self.index_manager = index_manager
        self.settings = QSettings("YourCompany", "FileOrganizerApp")
        self.directories = self.settings.value("watched_directories", [], type=list)
        self.observers = []
        self.init_ui()
        self.setup_watchers()

    def init_ui(self):
        layout = QVBoxLayout()

        self.directory_list = QListWidget()
        self.directory_list.itemClicked.connect(self.update_progress_for_directory)
        layout.addWidget(self.directory_list)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("0/0 images processed")
        layout.addWidget(self.progress_label)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Directory")
        self.remove_button = QPushButton("Remove Directory")
        self.process_button = QPushButton("Process Images")

        self.add_button.clicked.connect(self.add_directory)
        self.remove_button.clicked.connect(self.remove_directory)
        self.process_button.clicked.connect(self.process_directories)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.process_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_directories()

    def load_directories(self):
        for directory in self.directories:
            self.directory_list.addItem(directory)

    def add_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory and directory not in self.directories:
            self.directories.append(directory)
            self.directory_list.addItem(directory)
            self.setup_watcher(directory)
            self.save_directories()

    def remove_directory(self):
        current_item = self.directory_list.currentItem()
        if current_item:
            directory = current_item.text()
            self.directories.remove(directory)
            self.directory_list.takeItem(self.directory_list.row(current_item))
            self.remove_watcher(directory)
            self.save_directories()

    def update_progress_for_directory(self, item):
        directory = item.text()
        total_files = 0
        processed_files = 0

        # List of valid image extensions to consider for processing
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']

        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.splitext(file_path)[1].lower() not in valid_extensions:
                    continue
                total_files += 1
                if self.index_manager.is_file_processed(file_path):
                    processed_files += 1

        if total_files > 0:
            progress = int((processed_files / total_files) * 100)
            self.progress_bar.setValue(progress)
            self.progress_label.setText(f"{processed_files}/{total_files} images processed")

            if processed_files == total_files:
                self.process_button.setEnabled(False)
            else:
                self.process_button.setEnabled(True)
        else:
            self.progress_bar.setValue(0)
            self.progress_label.setText("No images found")
            self.process_button.setEnabled(False)

    def process_directories(self):
        current_item = self.directory_list.currentItem()
        if current_item:
            directory = current_item.text()

            # Determine files to process
            files_to_process = []
            valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']

            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.splitext(file_path)[1].lower() not in valid_extensions:
                        continue
                    if not self.index_manager.is_file_processed(file_path):
                        files_to_process.append(file_path)

            if not files_to_process:
                QMessageBox.information(self, "All Files Processed", "All files in the directory have already been processed.")
                return

            self.start_processing(files_to_process)

    def start_processing(self, files_to_process):
        self.worker = WorkerThread(files_to_process, self.update_progress, self.index_manager)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.start()

    def update_progress(self, processed, total):
        progress = int((processed / total) * 100)
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"{processed}/{total} images processed")

    def on_processing_finished(self):
        QMessageBox.information(self, "Processing Complete", "Directory processing has finished.")
        self.update_progress_for_directory(self.directory_list.currentItem())

    def setup_watchers(self):
        for directory in self.directories:
            self.setup_watcher(directory)

    def setup_watcher(self, directory):
        event_handler = FileHandler(self.process_new_file)
        observer = Observer()
        observer.schedule(event_handler, directory, recursive=True)
        observer.start()
        self.observers.append(observer)

    def remove_watcher(self, directory):
        for observer in self.observers:
            if observer.watches.get(directory):
                observer.unschedule_all()
                observer.stop()
                self.observers.remove(observer)
                break

    def process_new_file(self, file_path):
        try:
            if os.path.splitext(file_path)[1].lower() not in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                print(f"Skipping non-image file: {file_path}")
                return
            new_filename, description = self.worker.process_file(file_path)
            if new_filename:
                new_path = os.path.join(os.path.dirname(file_path), new_filename)
                self.index_manager.add_processed_file(file_path, new_path, new_filename, description)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while processing {file_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {file_path}: {e}")

    def save_directories(self):
        self.settings.setValue("watched_directories", self.directories)