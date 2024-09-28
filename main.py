import sys
import subprocess
from tkinter import messagebox, simpledialog
import socket
import tkinterdnd2
import os
import requests
import socket
import hashlib

import tkinter as Tk
def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)  # Отправляем пакет айпи
        return True
    except OSError:
        return False

GITHUB_REPO = "purplesmileguy/purplechat"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
EXPECTED_TAG_FORMAT = "v{}.{}.{}"

def get_current_version():
    try:
        # Return the current version
        return '1.0.1'
    except Exception as e:
        print(f"Error fetching current version: {e}")
        return '0.0.0'


def update_program():
    if not check_internet_connection():
        print("Нет подключения к интернету. Невозможно проверить обновления.")
        return

    try:
        response = requests.get(GITHUB_API_URL)
        release_info = response.json()
        latest_version_tag = release_info['tag_name']
        current_version = get_current_version()
        latest_version = latest_version_tag[1:]  # Исключаем первый символ 'v' из тега
        if latest_version > current_version:
            print("Доступно обновление.")
            choice = messagebox.askyesno("Обновление", "Доступно обновление. Хотите обновить программу?")
            if choice:
                print("Начинаем обновление...")
                assets = release_info['assets']
                asset = assets[0]  # Предполагаем, что первый ассет это файл программы
                download_url = asset['browser_download_url']
                new_file_path = os.path.join(os.getcwd(), "updated_program.py")
                with open(new_file_path, 'wb') as f:
                    response = requests.get(download_url)
                    f.write(response.content)
                print("Обновление завершено. Запускаем обновленную программу...")
                restart_program(new_file_path)
        else:
            pass
    except Exception as e:
        print(f"Произошла ошибка при обновлении программы: {e}")


def restart_program(new_file_path):
    try:
        if sys.platform.startswith('win'):
            # Для Windows
            subprocess.Popen([sys.executable, new_file_path])
        else:
            # Для Linux и macOS
            os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"Произошла ошибка при перезапуске программы: {e}")
    finally:
        sys.exit()

update_program()


import ctypes, webbrowser
import time

def flash_window(hwnd, count=3, timeout=500):
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

    if should_flash_window:
        FlashWindowEx(ctypes.byref(info))

# To trigger flashing, set should_flash_window to True where needed


# Переменная для контроля вызова функции
should_flash_window = False

# Ваш основной код
hwnd = 0  # Пример значения hwnd
#flash_window(hwnd)


import os

import random
import customtkinter
from datetime import datetime
import winsound
import threading
import tkinter.messagebox as messagebox
from tkinter import PhotoImage
from PIL import ImageTk, Image
import yaml
import string
import logging
import ctypes
import socket
import threading
import time
from tkinter import messagebox
import tkinter as tk

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s :  %(message)s')

script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, "pc.ico")
icon_pil = Image.open(icon_path)

hwnd = ctypes.windll.kernel32.GetConsoleWindow()

# Set the icon for the window
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('python.exe')
ctypes.windll.user32.SendMessageW(hwnd, 0x80, 0, icon_path)
ctypes.windll.kernel32.SetConsoleIcon(ctypes.windll.shell32.ExtractIconW(0, icon_path, 0))

from tqdm import tqdm
#for i in tqdm(range(int(9e6)),desc="Downloading update..."):
#                              pass


import socket
import threading
import customtkinter as ctk

from tkinter import scrolledtext
import socket
import threading
import subprocess
import threading
from tkinter import messagebox
from pyngrok import ngrok

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.broadcast(message, client_socket)
            except ConnectionResetError:
                break
        client_socket.close()
        self.clients.remove(client_socket)

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    client.close()
                    self.clients.remove(client)

    def run(self):
        print("Server is running...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()
class ChatRoom:
    def __init__(self, parent):
        self.parent = parent
        self.chat_text = customtkinter.CTkTextbox(master=self.parent, activate_scrollbars=False)
        self.chat_text.pack(expand=True, fill=tk.BOTH)

        self.chat_scrollbar = customtkinter.CTkScrollbar(master=self.parent, command=self.chat_text.yview)
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_text.configure(yscrollcommand=self.chat_scrollbar.set)

        self.message_entry = customtkinter.CTkEntry(master=self.parent, placeholder_text="Type a message...")
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.send_button = customtkinter.CTkButton(master=self.parent, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        self.server_socket = None  # This will be set later

    def send_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        if message:
            if self.server_socket:
                self.server_socket.send(message.encode('utf-8'))
class ChatRoomClient:
    def __init__(self, root, server_ip, server_port):
        self.root = root
        self.server_ip = server_ip
        self.server_port = server_port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))

        self.setup_ui()
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def setup_ui(self):
        self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill='both', expand=True)

        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack(side='left', fill='x', padx=(10, 0), pady=10, expand=True)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side='right', padx=10, pady=10)

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, message + '\n')
                    self.chat_area.config(state='disabled')
                    self.chat_area.yview(tk.END)
            except:
                break

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.socket.send(message.encode('utf-8'))
            self.message_entry.delete(0, tk.END)

def open_chat_room():
    chat_room_window = ctk.CTk()
    chat_room_window.geometry("400x300")
    chat_room_window.title("Chat Room")
    ChatRoomClient(chat_room_window, '127.0.0.1', 12345)
    chat_room_window.mainloop()


def create_room():
  logging.info('Action: create_room')
  create_room_window = customtkinter.CTk()
  create_room_window.geometry("380x340")
  create_room_window.title("Create Room")
  CreateRoomWindow(create_room_window)
  create_room_window.mainloop()

def generate_random_word():
    try:
        response = requests.get('https://random-word-api.herokuapp.com/word?number=1')
        response.raise_for_status()  # Проверка на наличие ошибок
        words = response.json()
        if words:
            return words[0]
        else:
            return ''.join(random.choices(string.ascii_letters, k=8))  # fallback
    except requests.RequestException:
        return ''.join(random.choices(string.ascii_letters, k=8))  # fallback
    
def generate_port():
   return str(random.randint(1024, 65535))
    
def create_join_room():
    logging.info('Action: create_join_room')
    join_room_window = customtkinter.CTk()
    join_room_window.geometry("380x340")
    join_room_window.title("Join Room")
    JoinRoomWindow(join_room_window)
    join_room_window.mainloop()

class CreateRoomWindow:
    def __init__(self, parent):
        logging.info('Creating CreateRoomWindow')

        self.parent = parent

        # Поле для ввода названия комнаты
        name_placeholder_text = "Room name"
        self.room_name_entry = customtkinter.CTkEntry(master=self.parent, placeholder_text=name_placeholder_text)
        self.room_name_entry.grid(row=1, column=0, padx=20, pady=20)

        # Подсказка о минимальной длине названия комнаты
        self.namelenght = customtkinter.CTkLabel(master=self.parent, text="Minimum 2 symbols", fg_color="transparent",
                                                font=("Helvetica", 15, "bold"))
        self.namelenght.grid(row=1, column=1, padx=20, pady=20, sticky="w")

        # Поле для ввода порта
        self.room_port_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT)
        self.room_port_entry.grid(row=2, column=0, padx=20, pady=20)

        # Подсказка о допустимом диапазоне портов
        self.portlenght = customtkinter.CTkLabel(master=self.parent, text="Port 1-65535", fg_color="transparent",
                                                font=("Helvetica", 15, "bold"))
        self.portlenght.grid(row=2, column=1, padx=20, pady=20, sticky="w")

        # Чекбокс для выбора, требуется ли пароль
        self.password_checkbox_var = customtkinter.BooleanVar(value=False)
        self.password_checkbox = customtkinter.CTkCheckBox(master=self.parent, text="Use Password",
                                                          variable=self.password_checkbox_var,
                                                          command=self.toggle_password_entry)
        self.password_checkbox.grid(row=3, column=0, padx=20, pady=20)

        # Поле для ввода пароля, которое отображается/скрывается в зависимости от состояния чекбокса
        self.password_entry = customtkinter.CTkEntry(master=self.parent)
        self.password_entry.grid(row=4, column=0, padx=20, pady=20)
        self.password_entry.grid_forget()  # Скрываем поле пароля по умолчанию

        self.create_button = customtkinter.CTkButton(master=self.parent, text="Create Room", command=self.create_room,
                                                      hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
        self.create_button.grid(row=5, column=0, padx=20, pady=20)
        self.create_button.configure(state="disabled")

        self.room_name_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_room_name), "%P"))
        self.room_port_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_room_port), "%P"))
        self.password_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_password), "%P"))

        default_port = "12345"
        self.room_port_entry.insert(0, default_port)

        default_room_name = "My Room"
        self.room_name_entry.insert(0, default_room_name)

    def toggle_password_entry(self):
        if self.password_checkbox_var.get():
            self.password_entry.grid(row=4, column=0, padx=20, pady=20)
        else:
            self.password_entry.grid_forget()

    def validate_room_name(self, name):
        if len(name) < 2:
            self.create_button.configure(state="disabled")
            return True
        elif len(name) > 12:
            truncated_name = name[:12]
            self.room_name_entry.delete(12, "end")
            return False
        else:
            self.create_button.configure(state="normal")
            return True

    def validate_room_port(self, port):
        if len(port) <= 5:
            return True
        if not port.isdigit():
            return False
        port = int(port)
        if port < 1 or port > 65535:
            messagebox.showerror("Invalid Port", "Port must be between 1 and 65535")
            return False
        else:
            return True

    def validate_password(self, password):
        if len(password) > 12:
            password = password[:12]
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.insert(0, password)
            return True
        else:
            return True

    def create_room(self):
        room_name = self.room_name_entry.get()
        room_port = self.room_port_entry.get()
        password = None

        if self.password_checkbox_var.get():
            password = self.password_entry.get()
            if not self.validate_password(password):
                messagebox.showerror("Invalid Password", "Please enter a valid password.")
                return

        print("Room Name:", room_name)
        print("Room Port:", room_port)
        if password:
            print("Room Password:", password)
        # Запуск сервера
        server = ChatServer(port=int(room_port))
        threading.Thread(target=server.run, daemon=True).start()

        # Запуск ngrok туннеля
        self.start_ngrok(room_port)

        # Открытие окна чата
        chat_room_window = customtkinter.CTk()
        chat_room_window.geometry("580x540")
        chat_room_window.title("Chat Room - " + room_name)
        ChatRoom(chat_room_window)
        chat_room_window.mainloop()

    def start_ngrok(self, room_port):
        def run_ngrok():
            try:
                # Используем TCP-туннель вместо HTTP
                tcp_tunnel = ngrok.connect(room_port, "tcp")
                ngrok_url = tcp_tunnel.public_url
                print("ngrok URL:", ngrok_url)
            except Exception as e:
                print("Error starting ngrok:", e)
            
        ngrok_thread = threading.Thread(target=run_ngrok)
        ngrok_thread.start()
    
    def extract_ngrok_url(self, ngrok_output):
        for line in ngrok_output.splitlines():
            if "tcp://" in line:
                return line.split("://")[1]
        return ""
import customtkinter
import tkinter as tk
from tkinter import messagebox
import logging

import tkinter as tk
from tkinter import messagebox
import customtkinter
import logging

class JoinRoomWindow:
    def __init__(self, parent):
        logging.info('Creating JoinRoomWindow')

        self.parent = parent

        # Поле для ввода URL комнаты
        self.room_url_entry = customtkinter.CTkEntry(master=self.parent, placeholder_text="Room URL")
        self.room_url_entry.grid(row=0, column=0, padx=20, pady=20)

        # Чекбокс для выбора, требуется ли пароль
        self.password_checkbox_var = customtkinter.BooleanVar(value=False)
        self.password_checkbox = customtkinter.CTkCheckBox(master=self.parent, text="Use Password", font=("Helvetica", 15, "bold"),
                                                          variable=self.password_checkbox_var, command=self.toggle_password_entry)
        self.password_checkbox.grid(row=1, column=0, padx=20, pady=20)

        # Поле для ввода пароля, которое отображается/скрывается в зависимости от состояния чекбокса
        self.password_entry = customtkinter.CTkEntry(master=self.parent, placeholder_text="Password", show='*')
        self.password_entry.grid(row=2, column=0, padx=20, pady=20)
        self.password_entry.grid_forget()  # Скрываем поле пароля по умолчанию

        # Кнопка для подключения к комнате
        self.join_button = customtkinter.CTkButton(master=self.parent, text="Join Room", command=self.join_room,
                                                 hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
        self.join_button.grid(row=3, column=0, padx=20, pady=20)

        # Настройка валидации ввода
        self.room_url_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_room_url), "%P"))

    def toggle_password_entry(self):
        if self.password_checkbox_var.get():
            self.password_entry.grid(row=2, column=0, padx=20, pady=20)
        else:
            self.password_entry.grid_forget()

    def join_room(self):
        room_url = self.room_url_entry.get()
        password = self.password_entry.get() if self.password_checkbox_var.get() else None

        # Проверка корректности URL перед попыткой подключения
        if not self.validate_room_url(room_url):
            messagebox.showerror("Invalid Room URL", "Please enter a valid room URL.")
            return

        # Проверка пароля, если требуется
        if self.password_checkbox_var.get() and not password:
            messagebox.showerror("Password Required", "Please enter a password for the room.")
            return

        print("Room URL:", room_url)
        if password:
            print("Room Password:", password)
        # Добавьте логику для подключения к серверу и открытия окна чата

    def validate_room_url(self, url):
        # Простая проверка длины URL. Вы можете добавить дополнительную логику проверки.
        if len(url) > 100:
            return False
        # Можно добавить дополнительную валидацию для URL
        return True



def error_sound():
    threading.Thread(target=play_sound, args=(1000, 500)).start()

def play_sound(frequency, duration):
    winsound.Beep(frequency, duration)

NightTrain = os.path.join(script_dir, "NightTrain.json")
NeonBanana = os.path.join(script_dir, "NeonBanana.json")
customtkinter.set_ctk_parent_class(tkinterdnd2.Tk)
#customtkinter.deactivate_automatic_dpi_awareness()
customtkinter.set_appearance_mode("dark")


username1 = "user" + str(random.randint(0, 9999))

save_file = "data.yaml"  # Change save file extension to .yaml

def update_username(event=None):
    global username

    new_username = label_1.get()

    if len(new_username) < 1:
        messagebox.showinfo("Error", "Username must contain at least 1 character")
        label_1.configure(fg_color="#c94040")
        error_sound()
        label_1.delete(0, customtkinter.END)
        new_username = "user" + str(random.randint(0, 9999))
        label_1.insert(0, new_username)
        update_username()
    else:
        label_1.configure(fg_color="black")

        # Load existing data from YAML file
        with open(save_file, "r") as file:
            data = yaml.safe_load(file)

        # Update the username in the loaded data
        data["username"] = new_username

        # Save the updated data back to YAML file
        with open(save_file, "w") as file:
            yaml.dump(data, file)

        username = new_username


# Function to initialize configuration
def initialize_config():
    if not os.path.exists(save_file):
        # If file does not exist, create default configuration
        username = "user" + str(random.randint(0, 9999))
        config = {
            "username": username,
        }
        with open(save_file, "w") as file:
            yaml.dump(config, file)
    else:
        # If file exists, load existing configuration
        with open(save_file, "r") as file:
            data = yaml.safe_load(file)
            username = data.get("username", "user")
    return username

# Function to load and apply theme
def load_theme():
    global current_theme
    if os.path.exists(save_file):
        with open(save_file, "r") as file:
            data = yaml.safe_load(file)
            current_theme = data.get("theme", "NightTrain")

    if current_theme == "NightTrain":
        customtkinter.set_default_color_theme(NightTrain)
    elif current_theme == "NeonBanana":
        customtkinter.set_default_color_theme(NeonBanana)
    else:
        logging.warning("Unknown theme in data.yaml: %s", current_theme)
        current_theme = "NightTrain"
        customtkinter.set_default_color_theme(NightTrain)

def change_theme():
    global current_theme
    if current_theme == "NightTrain":
        current_theme = "NeonBanana"
        customtkinter.set_default_color_theme(NeonBanana)
    elif current_theme == "NeonBanana":
        current_theme = "NightTrain"
        customtkinter.set_default_color_theme(NightTrain)
    else:
        print("Unknown theme:", current_theme)

    # Update the theme in the YAML file
    with open(save_file, "r") as file:
        data = yaml.safe_load(file)
    data["theme"] = current_theme
    with open(save_file, "w") as file:
        yaml.dump(data, file)
    
    logging.info('Theme changed to %s', current_theme)
    # Optionally, you can implement a way to refresh the GUI without restarting the app

    os.execv(sys.executable, [sys.executable] + sys.argv)
    app.destroy()

import base64

def xor_cipher(text, key):
    return ''.join(chr(ord(c) ^ key) for c in text)

def decrypt_text(encoded_text, key):
    encrypted = base64.b64decode(encoded_text).decode()
    return xor_cipher(encrypted, key)

key = 42  # Ключ, используемый для XOR

# Ваш зашифрованный текст
encoded_text = "GEEaYWB/G0RmQE5rR0NaX19mXE1eQGkfaXtsdR1ZTB1YcGRbH3xFHBl5QWBkaEIZZg=="

# Дешифрование
decrypted = decrypt_text(encoded_text, key)
print("Decrypted:", decrypted)

# Установка токена ngrok
ngrok.set_auth_token(decrypted)

username = initialize_config()
load_theme()    
print(f"Username: {username}")
print(f"Current Theme: {current_theme}")

app = customtkinter.CTk()
app.geometry("400x260")
app.title("PythonChat")

label_1 = customtkinter.CTkEntry(master=app, justify=customtkinter.LEFT)
label_1.pack(pady=1)
label_1.grid(row=0, column=0, padx=20, pady=20)
label_1.insert(0, username)

label_1.bind("<KeyRelease>", update_username)

joinRoomButton = customtkinter.CTkButton(app, text="Join room", command=create_join_room, hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
joinRoomButton.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

import sys

changeTButton = customtkinter.CTkButton(app, text="Change theme", command=change_theme, hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
changeTButton.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="w")

createRoomButton = customtkinter.CTkButton(app, text="Create room", command=create_room, hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
createRoomButton.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")

info_frame = customtkinter.CTkFrame(master=app, fg_color="transparent", border_width=0)
info_frame.grid(row=0, column=1, padx=20, pady=(20, 20), sticky="e")

time_label = customtkinter.CTkLabel(master=info_frame, text="", font=("Helvetica", 14))
time_label.pack(side="top")

date_label = customtkinter.CTkLabel(master=info_frame, text="", font=("Helvetica", 14))
date_label.pack(side="bottom")

def update_time_and_date():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    time_label.configure(text="Time: " + current_time)
    date_label.configure(text="Date: " + current_date)
    app.after(1000, update_time_and_date)  

update_time_and_date()
# Флаг, чтобы отслеживать, было ли уже показано сообщение о доступности интернета
internet_connection_shown = False

def check_internet_periodically():
    global internet_connection_shown
    
    while True:
        if check_internet_connection():
            internet_status = "Yes"  # Internet connection is available
        else:
            internet_status = "No"   # No internet connection
        
        # Update window title with internet status
        app.title(f"PythonChat (Connection: {internet_status})")
        
        time.sleep(1)  # Wait 1 second before the next check

# Запускаем проверку доступа к интернету в отдельном потоке
internet_thread = threading.Thread(target=check_internet_periodically)
internet_thread.daemon = True  # Устанавливаем демонический флаг, чтобы поток завершался при закрытии приложения
internet_thread.start()

icon = ImageTk.PhotoImage(icon_pil)
app.iconphoto(True, icon)
app.wm_iconbitmap()
app.minsize(400, 260)
app.maxsize(400, 260)
app.mainloop()