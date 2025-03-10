import socket
import requests
import yaml
import random
import sys
import subprocess
import os
import winsound
import threading
import time
from config import save_file, GITHUB_API_URL
from PyQt6.QtWidgets import QMessageBox
from qt_material import apply_stylesheet

def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        return False

def update_program(parent_widget=None):
    if not check_internet_connection():
        print("Нет интернета для проверки обновлений.")
        return
    try:
        response = requests.get(GITHUB_API_URL)
        release_info = response.json()
        latest_version_tag = release_info['tag_name']
        current_version = get_current_version()
        latest_version = latest_version_tag[1:]
        if latest_version > current_version:
            print("Доступно обновление.")
            if parent_widget and QMessageBox.question(parent_widget, "Обновление", "Доступно обновление. Хотите обновить программу?") == QMessageBox.StandardButton.Yes:
                print("Начинаем обновление...")
                assets = release_info['assets']
                asset = assets[0]
                download_url = asset['browser_download_url']
                new_file_path = os.path.join(os.getcwd(), "updated_program.py")
                with open(new_file_path, 'wb') as f:
                    response = requests.get(download_url)
                    f.write(response.content)
                print("Обновление завершено. Запускаем обновленную программу...")
                restart_program(new_file_path)
    except Exception as e:
        print(f"Ошибка при обновлении: {e}")

def get_current_version():
    return '1.0.1'

def restart_program(new_file_path):
    try:
        if sys.platform.startswith('win'):
            subprocess.Popen([sys.executable, new_file_path])
        else:
            os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"Ошибка при перезапуске: {e}")
    finally:
        sys.exit()

def initialize_config():
    default_config = {"username": "user" + str(random.randint(0, 9999)), "theme": "dark_teal.xml"}
    if not os.path.exists(save_file):
        with open(save_file, "w") as file:
            yaml.dump(default_config, file)
        return default_config
    else:
        try:
            with open(save_file, "r") as file:
                config = yaml.safe_load(file)
            if config is None:  # Если файл пустой
                config = default_config
                with open(save_file, "w") as file:
                    yaml.dump(config, file)
            return config
        except yaml.YAMLError as e:
            print(f"Ошибка чтения конфигурации: {e}")
            return default_config

def load_theme(app):
    config = initialize_config()
    current_theme = config.get("theme", "dark_teal.xml")
    apply_stylesheet(app, theme=current_theme)

def change_theme(app):
    config = initialize_config()
    current_theme = config.get("theme", "dark_teal.xml")
    new_theme = "light_pink.xml" if current_theme == "dark_teal.xml" else "dark_teal.xml"
    config["theme"] = new_theme
    with open(save_file, "w") as file:
        yaml.dump(config, file)
    apply_stylesheet(app, theme=new_theme)

def error_sound():
    threading.Thread(target=play_sound, args=(1000, 500)).start()

def play_sound(frequency, duration):
    winsound.Beep(frequency, duration)

def flash_window(hwnd, count=3, timeout=500):
    import ctypes
    FLASHWINFO = [
        ("cbSize", ctypes.c_uint),
        ("hwnd", ctypes.c_void_p),
        ("dwFlags", ctypes.c_uint),
        ("uCount", ctypes.c_uint),
        ("dwTimeout", ctypes.c_uint)
    ]
    FlashWindowEx = ctypes.windll.user32.FlashWindowEx
    FLASHW_TRAY = 0x00000002
    FLASHW_CAPTION = 0x00000001
    FLASHW_TIMERNOFG = 0x0000000C

    class FLASHWINFO(ctypes.Structure):
        _fields_ = FLASHWINFO

    info = FLASHWINFO()
    info.cbSize = ctypes.sizeof(FLASHWINFO)
    info.hwnd = hwnd
    info.dwFlags = FLASHW_TRAY | FLASHW_CAPTION | FLASHW_TIMERNOFG
    info.uCount = count
    info.dwTimeout = timeout

    FlashWindowEx(ctypes.byref(info))