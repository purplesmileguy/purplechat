import customtkinter as ctk
from gui import MainWindow
from utils import load_theme, check_internet_connection, update_program, flash_window
from config import icon_path
import threading
import time
import sys

def check_internet_periodically(app):
    while True:
        if check_internet_connection():
            internet_status = "Yes"
        else:
            internet_status = "No"
        app.title(f"PythonChat (Connection: {internet_status})")
        time.sleep(1)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    load_theme()
    update_program()
    app = ctk.CTk()
    app.geometry("400x260")
    app.title("PythonChat")
    app.iconbitmap(icon_path)
    MainWindow(app)
    internet_thread = threading.Thread(target=check_internet_periodically, args=(app,))
    internet_thread.daemon = True
    internet_thread.start()
    app.mainloop()