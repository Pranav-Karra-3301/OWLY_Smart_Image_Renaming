from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QListWidget, QListWidgetItem)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

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
        
        # File list
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.show_file_details)
        results_layout.addWidget(self.file_list)

        # File details
        details_layout = QVBoxLayout()
        self.image_preview = QLabel()
        details_layout.addWidget(self.image_preview)
        
        self.file_info = QLabel("File information will appear here")
        details_layout.addWidget(self.file_info)

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
            item = QListWidgetItem(result['new_filename'])
            item.setData(Qt.ItemDataRole.UserRole, result)
            self.file_list.addItem(item)

    def show_file_details(self, item):
        file_data = item.data(Qt.ItemDataRole.UserRole)
        self.image_preview.setPixmap(QPixmap(file_data['new_path']).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        self.file_info.setText(
            f"Filename: {file_data['new_filename']}\n"
            f"Original Filename: {file_data['original_filename']}\n"
            f"Path: {file_data['new_path']}\n"
            f"Description: {file_data.get('description', 'No description available')}\n"
            f"Processing Date: {file_data.get('processing_date', 'Unknown')}"
        )