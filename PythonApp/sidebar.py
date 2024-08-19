# sidebar.py
from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtGui import QIcon

class Sidebar(QListWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                border: none;
            }
            QListWidget::item {
                color: white;
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #2d2d2d;
            }
        """)

        items = [
            ("Search", "search_icon.png"),
            ("Queue", "queue_icon.png"),
            ("Directories", "folder_icon.png"),
            ("Preferences", "preferences_icon.png"),
            ("API key", "api_key_icon.png")
        ]

        for text, icon in items:
            item = QListWidgetItem(QIcon(f"icons/{icon}"), text)
            self.addItem(item)