# api_key_page.py
import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import QSettings

class APIKeyPage(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("YourCompany", "FileOrganizerApp")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setText(self.settings.value("openai_api_key", ""))
        
        save_button = QPushButton("Save API Key")
        save_button.clicked.connect(self.save_api_key)
        
        layout.addWidget(QLabel("Enter your OpenAI API Key:"))
        layout.addWidget(self.api_key_input)
        layout.addWidget(save_button)
        
        self.setLayout(layout)

    def save_api_key(self):
        api_key = self.api_key_input.text()
        self.settings.setValue("openai_api_key", api_key)
        
        # Update config.json
        try:
            with open('config.json', 'r+') as f:
                config = json.load(f)
                config['openai_api_key'] = api_key
                f.seek(0)
                json.dump(config, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            with open('config.json', 'w') as f:
                json.dump({'openai_api_key': api_key}, f, indent=4)