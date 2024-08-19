# directories_page.py

import os
import subprocess
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QFileDialog, QMessageBox, QListWidgetItem)
from PyQt6.QtCore import QThread, pyqtSignal, QSettings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WorkerThread(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, directory):
        super().__init__()
        self.directory = directory

    def run(self):
        try:
            total_files = sum([len(files) for r, d, files in os.walk(self.directory)])
            processed_files = 0
            
            for root, dirs, files in os.walk(self.directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.basename(file_path) == '.DS_Store':
                        print(f"Skipping .DS_Store file: {file_path}")
                        continue
                    subprocess.run(["python", "scripts/advanced_base64.py", file_path], check=True)
                    subprocess.run(["python", "scripts/rename_files_base64.py", file_path], check=True)
                    processed_files += 1
                    self.progress.emit(processed_files, total_files)
            
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the scripts: {e}")
        self.finished.emit()

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
        layout.addWidget(self.directory_list)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Directory")
        remove_button = QPushButton("Remove Directory")
        process_button = QPushButton("Process Directories")

        add_button.clicked.connect(self.add_directory)
        remove_button.clicked.connect(self.remove_directory)
        process_button.clicked.connect(self.process_directories)

        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(process_button)

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

    def process_directories(self):
        if not self.directories:
            QMessageBox.warning(self, "No Directories", "Please add directories to process.")
            return

        for directory in self.directories:
            self.process_directory_signal.emit(directory)

    def process_directory(self, directory):
        self.worker = WorkerThread(directory)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.start()

    def update_progress(self, processed, total):
        # Update progress in Queue page
        pass

    def on_processing_finished(self):
        QMessageBox.information(self, "Processing Complete", "Directory processing has finished.")

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
            if os.path.basename(file_path) == '.DS_Store':
                print(f"Skipping .DS_Store file: {file_path}")
                return
            subprocess.run(["python", "scripts/advanced_base64.py", file_path], check=True)
            subprocess.run(["python", "scripts/rename_files_base64.py", file_path], check=True)
            self.index_manager.add_to_index(file_path)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while processing {file_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {file_path}: {e}")

    def save_directories(self):
        self.settings.setValue("watched_directories", self.directories)