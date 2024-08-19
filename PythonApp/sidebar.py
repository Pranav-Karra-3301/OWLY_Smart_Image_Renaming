from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtGui import QIcon

class Sidebar(QListWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        items = [
            ("Search", "assets/search_icon.png"),
            ("Directories", "assets/folder_icon.png"),
            ("Preferences", "assets/preferences_icon.png"),
            ("API Key", "assets/api_key_icon.png")
        ]

        for index, (text, icon) in enumerate(items):
            item = QListWidgetItem(QIcon(icon), text)
            self.addItem(item)
        
        # Ensure that the sidebar starts by selecting the first item
        self.setCurrentRow(0)