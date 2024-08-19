# preferences_page.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PreferencesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Preferences Page - To be implemented"))
        self.setLayout(layout)