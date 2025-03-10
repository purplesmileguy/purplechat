import socket
import requests
import yaml
import random
import sys
import subprocess
import customtkinter
from tkinter import messagebox
import os
import winsound
import threading
import time
from config import save_file, NightTrain, NeonBanana, GITHUB_API_URL

def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        return False

def update_program():
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
            if messagebox.askyesno("Обновление", "Доступно обновление. Хотите обновить программу?"):
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
    if not os.path.exists(save_file):
        username = "user" + str(random.randint(0, 9999))
        config = {"username": username, "theme": "NightTrain"}
        with open(save_file, "w") as file:
            yaml.dump(config, file)
    else:
        with open(save_file, "r") as file:
            config = yaml.safe_load(file)
    return config

def load_theme():
    config = initialize_config()
    current_theme = config.get("theme", "NightTrain")
    if current_theme == "NightTrain":
        customtkinter.set_default_color_theme(NightTrain)
    elif current_theme == "NeonBanana":
        customtkinter.set_default_color_theme(NeonBanana)
    else:
        customtkinter.set_default_color_theme(NightTrain)

def change_theme():
    config = initialize_config()
    current_theme = config.get("theme", "NightTrain")
    new_theme = "NeonBanana" if current_theme == "NightTrain" else "NightTrain"
    config["theme"] = new_theme
    with open(save_file, "w") as file:
        yaml.dump(config, file)
    os.execv(sys.executable, [sys.executable] + sys.argv)

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