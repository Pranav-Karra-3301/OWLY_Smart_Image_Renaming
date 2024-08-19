import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from main_window import MainWindow
from index_manager import IndexManager

def main():
    app = QApplication(sys.argv)
    
    # Set the app icon
    icon = QIcon('assets/icon.icns')
    app.setWindowIcon(icon)
    
    # On macOS, set the dock icon
    if sys.platform == 'darwin':
        app.setWindowIcon(icon)
    
    # Create the index manager
    app.setApplicationName("Owly")
    index_manager = IndexManager()
    
    # Create and show the main window
    main_window = MainWindow(index_manager)
    main_window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()