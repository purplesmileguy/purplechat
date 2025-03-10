import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from gui import MainWindow
from utils import load_theme, check_internet_connection, update_program, flash_window
from config import icon_path
import threading
import time

def check_internet_periodically(app):
    while True:
        if check_internet_connection():
            internet_status = "Yes"
        else:
            internet_status = "No"
        app.setWindowTitle(f"PythonChat (Connection: {internet_status})")
        time.sleep(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_theme(app)
    update_program()
    window = MainWindow(app)  # Передаем app в MainWindow
    window.setWindowIcon(QIcon(icon_path))
    window.show()
    internet_thread = threading.Thread(target=check_internet_periodically, args=(window,))
    internet_thread.daemon = True
    internet_thread.start()
    sys.exit(app.exec())