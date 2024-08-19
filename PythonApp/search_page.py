import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QListWidget, QListWidgetItem, QPushButton)
from PyQt6.QtGui import QPixmap, QClipboard
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

class SearchPage(QWidget):
    def __init__(self, index_manager):
        super().__init__()
        self.index_manager = index_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.search)
        search_layout.addWidget(self.search_bar)
        layout.addLayout(search_layout)

        # Results area
        results_layout = QHBoxLayout()

        # File list (Sidebar)
        self.file_list = QListWidget()
        self.file_list.setFixedWidth(200)  # Adjust the sidebar width to fit items
        self.file_list.itemClicked.connect(self.show_file_details)
        results_layout.addWidget(self.file_list)

        # File details
        details_layout = QVBoxLayout()

        # Larger image preview
        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setFixedHeight(400)  # Set a larger height for the image preview
        self.image_preview.setFixedWidth(600)  # Set a larger width for the image preview
        details_layout.addWidget(self.image_preview)

        # Image name
        self.file_name_label = QLabel()
        self.file_name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        details_layout.addWidget(self.file_name_label)

        # Description block
        self.description_title = QLabel("Description:")
        self.description_title.setStyleSheet("font-weight: bold;")
        details_layout.addWidget(self.description_title)

        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        details_layout.addWidget(self.description_label)

        # Path and other information
        self.file_info = QLabel()
        self.file_info.setWordWrap(True)
        details_layout.addWidget(self.file_info)

        # Buttons
        button_layout = QHBoxLayout()
        self.copy_image_button = QPushButton("Copy Image")
        self.copy_image_button.clicked.connect(self.copy_image_to_clipboard)
        button_layout.addWidget(self.copy_image_button)

        self.show_in_finder_button = QPushButton("Show in Finder")
        self.show_in_finder_button.clicked.connect(self.show_in_finder)
        button_layout.addWidget(self.show_in_finder_button)

        details_layout.addLayout(button_layout)

        results_layout.addLayout(details_layout)

        layout.addLayout(results_layout)

        self.setLayout(layout)

        # Display all files by default, sorted by process date (recent first)
        self.search("")

    def search(self, query=""):
        results = self.index_manager.search(query)
        self.file_list.clear()

        # Sort results by processing date, most recent first
        sorted_results = sorted(results, key=lambda x: x.get('processing_date', ''), reverse=True)

        for result in sorted_results:
            if query.lower() in result.get('description', '').lower() or query.lower() in result.get('new_filename', '').lower():
                item = QListWidgetItem(result['new_filename'])
                item.setData(Qt.ItemDataRole.UserRole, result)
                self.file_list.addItem(item)

    def show_file_details(self, item):
        file_data = item.data(Qt.ItemDataRole.UserRole)

        # Scale the image to fit the larger preview space
        pixmap = QPixmap(file_data['new_path'])
        self.image_preview.setPixmap(pixmap.scaled(self.image_preview.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        # Update the name, description, and other information
        self.file_name_label.setText(file_data['new_filename'])
        self.description_label.setText(file_data.get('description', 'No description available'))
        self.file_info.setText(
            f"<b>Path:</b> {file_data['new_path']}<br><br>"
            f"<span style='color:gray'><i>Original Filename:</i> {file_data['original_filename']}<br>"
            f"<i>Processing Date:</i> {file_data.get('processing_date', 'Unknown')}</span>"
        )

        # Store the current file path for buttons to use
        self.current_file_path = file_data['new_path']

    def copy_image_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(QPixmap(self.current_file_path))
        print("Image copied to clipboard.")

    def show_in_finder(self):
        if os.path.exists(self.current_file_path):
            os.system(f'open -R "{self.current_file_path}"')
        else:
            print("File not found.")