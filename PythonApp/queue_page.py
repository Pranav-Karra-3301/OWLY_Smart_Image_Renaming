# queue_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QMovie

class QueuePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Waiting for process to start...")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.loading_label = QLabel()
        self.loading_movie = QMovie("loading.gif")  # Make sure to have a loading.gif in your project directory
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setVisible(False)
        layout.addWidget(self.loading_label)

        self.setLayout(layout)

    @pyqtSlot()
    def start_processing(self):
        self.status_label.setText("Processing files...")
        self.progress_bar.setVisible(True)
        self.loading_label.setVisible(True)
        self.loading_movie.start()

    @pyqtSlot(int, int)
    def update_progress(self, current, total):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.status_label.setText(f"Processing file {current} of {total}")

    @pyqtSlot(str)
    def show_completion_message(self, message):
        self.status_label.setText(message)
        self.progress_bar.setVisible(False)
        self.loading_label.setVisible(False)
        self.loading_movie.stop()