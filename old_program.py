import os
import sys
import subprocess
import requests
from tkinter import messagebox
import traceback

GITHUB_REPO = "purplesmileguy/purplechat"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

def get_current_version():
    # Здесь вы можете реализовать код для получения текущей версии вашей программы
    # Например, версия может быть храниться в каком-то файле или переменной
    # Возвращаем текущую версию (замените это на ваш реальный способ получения версии)
    return '1.1.0'

def compare_versions(current_version, latest_version):
    current_version_parts = [int(part) for part in current_version.split('.')]
    latest_version_parts = [int(part) for part in latest_version.split('.')]
    # Сравниваем каждый компонент версии
    for curr, latest in zip(current_version_parts, latest_version_parts):
        if curr < latest:
            return True
        elif curr > latest:
            return False
    return False

def update_program():
    try:
        current_version = get_current_version()
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        latest_release = response.json()

        if compare_versions(current_version, latest_release['tag_name']):
            # Получаем ссылку на файлы обновления
            assets = latest_release['assets']
            # Перебираем все файлы обновления
            for asset in assets:
                asset_url = asset['browser_download_url']
                filename = asset['name']
                # Проверяем, является ли файл программы файлом main.py
                if filename == 'main.py':
                    # Получаем расширение текущего файла программы
                    current_file_extension = os.path.splitext(sys.argv[0])[1].lower()
                    # Получаем расширение нового файла программы
                    new_file_extension = os.path.splitext(filename)[1].lower()
                    # Определяем путь к новому файлу
                    new_file_path = os.path.join(os.getcwd(), filename)
                    # Загружаем новый файл
                    response = requests.get(asset_url)
                    with open(new_file_path, 'wb') as f:
                        f.write(response.content)
                    # Если расширения файлов совпадают, заменяем текущий файл программы
                    if current_file_extension == new_file_extension:
                        current_file_path = os.path.abspath(sys.argv[0])
                        os.replace(new_file_path, current_file_path)
                        messagebox.showinfo("Обновление", "Программа успешно обновлена. Пожалуйста, перезапустите программу.")
                        restart_program(current_file_path)
                        return
                    else:
                        messagebox.showinfo("Обновление", "Программа успешно обновлена. Новая версия программы другого формата была загружена.")
                        restart_program(new_file_path)
                        return
        else:
            messagebox.showinfo("Обновление", "У вас уже последняя версия программы.")
    except Exception as e:
        messagebox.showerror("Ошибка обновления", f"Произошла ошибка при обновлении программы:\n\n{traceback.format_exc()}")

def restart_program(new_file_path):
    try:
        if sys.platform.startswith('win'):
            # Для Windows
            subprocess.Popen([sys.executable, new_file_path])
        else:
            # Для Linux и macOS
            os.execl(sys.executable, sys.executable, new_file_path)
    except Exception as e:
        messagebox.showerror("Ошибка перезапуска", f"Произошла ошибка при перезапуске программы:\n\n{traceback.format_exc()}")
    finally:
        sys.exit()

# Вызов функции для проверки обновлений
update_program()
import os

import random
import customtkinter
import tkinterDnD
from datetime import datetime
import winsound
import threading
import tkinter.messagebox as messagebox
from tkinter import PhotoImage
from PIL import ImageTk, Image
import yaml  # Import PyYAML
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


class ChatRoom:
    def __init__(self, parent):
        self.parent = parent
        self.room_name_entry = customtkinter.CTkEntry(master=self.parent)
        self.room_name_entry.grid(row=1, column=0, padx=20, pady=20)
        
        app = customtkinter.CTk()
        app.geometry("400x260")
        app.title("PythonChat")
        
        label_1 = customtkinter.CTkLabel(master=app, justify=customtkinter.LEFT,textvariable=username)
        label_1.pack(pady=1)
        label_1.grid(row=0, column=0, padx=20, pady=20)


def join_room():
    logging.info('Action: join_room')
    print("button pressed")
    threading.Thread(target=play_sound, args=(1000, 500)).start()

def create_room():
  logging.info('Action: create_room')
  create_room_window = customtkinter.CTk()
  create_room_window.geometry("380x340")
  create_room_window.title("Create Room")
  CreateRoomWindow(create_room_window)
  create_room_window.mainloop()


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
        name_placeholder_text = "Room name"

        self.parent = parent
        
        self.room_name_entry = customtkinter.CTkEntry(master=self.parent,placeholder_text=name_placeholder_text)
        self.room_name_entry.grid(row=1, column=0, padx=20, pady=20)

        self.namelenght = customtkinter.CTkLabel(master=self.parent, text="Minimum 2 symbols", fg_color="transparent",
                                                 font=("Helvetica", 15, "bold"))
        self.namelenght.grid(row=1, column=1, padx=20, pady=20, sticky="w")

        self.room_port_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT)
        self.room_port_entry.grid(row=2, column=0, padx=20, pady=20)
        
        self.portlenght = customtkinter.CTkLabel(master=self.parent, text="Port 1-65535", fg_color="transparent",
                                             font=("Helvetica", 15, "bold"))
        self.portlenght.grid(row=2, column=1, padx=20, pady=20, sticky="w")

        self.password_checkbox_var = customtkinter.BooleanVar(value=True)
        self.password_checkbox = customtkinter.CTkCheckBox(master=self.parent, text="Use Password",
                                                           variable=self.password_checkbox_var,
                                                           command=self.toggle_password_entry)
        
        self.password_checkbox.grid(row=3, column=0, padx=20, pady=20)
        #password_placeholder_text = "Password" placeholder_text=password_placeholder_text,
        self.password_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT, state="normal")
        self.password_entry.grid(row=3, column=1, padx=20, pady=20)

        self.create_button = customtkinter.CTkButton(master=self.parent, text="Create Room", command=self.create_room,
                                                      hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
        self.create_button.grid(row=5, column=0, padx=20, pady=20)
        self.create_button.configure(state="disabled")

        self.room_name_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_room_name), "%P"))
        self.room_port_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_room_port), "%P"))
        self.password_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_password), "%P"))
        self.password_entry.insert(0, self.generate_password())

    def toggle_password_entry(self):
        if self.password_checkbox_var.get():
            self.password_entry.configure(state="normal")
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.grid()
            self.password_entry.insert(0, self.generate_password())
        else:
            self.password_entry.pack()
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.configure(state="readonly")

    def generate_password(self):
        password_length = 3
        password_characters = string.ascii_letters + string.digits
        return ''.join(random.choice(password_characters) for _ in range(password_length))
    #generate_password(self)
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
        if len(port) <= 5:  # Если длина порта меньше или равна 5 символам
            return True     # Пропускаем проверку, так как порт уже установлен и состоит из 5 символов
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
        create_room_window = customtkinter.CTk()
        create_room_window.geometry("580x540")
        create_room_window.title("Sigma")
        ChatRoom(create_room_window)
        create_room_window.mainloop()
        if password:
            print("Room Password:", password)

class JoinRoomWindow:
    def __init__(self, parent):
        logging.info('Creating CreateRoomWindow')

        self.parent = parent
        self.room_name_entry = customtkinter.CTkEntry(master=self.parent)
        self.room_name_entry.grid(row=1, column=0, padx=20, pady=20)

        self.namelenght = customtkinter.CTkLabel(master=self.parent, text="Minimum 2 symbols", fg_color="transparent",
                                                 font=("Helvetica", 15, "bold"))
        self.namelenght.grid(row=1, column=1, padx=20, pady=20, sticky="w")

        self.room_port_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT)
        self.room_port_entry.grid(row=2, column=0, padx=20, pady=20)
        
        self.portlenght = customtkinter.CTkLabel(master=self.parent, text="Port 1-65535", fg_color="transparent",
                                             font=("Helvetica", 15, "bold"))
        self.portlenght.grid(row=2, column=1, padx=20, pady=20, sticky="w")

        self.password_checkbox_var = customtkinter.BooleanVar(value=True)
        self.password_checkbox = customtkinter.CTkCheckBox(master=self.parent, text="Use Password",
                                                           variable=self.password_checkbox_var,
                                                           command=self.toggle_password_entry)
        
        self.password_checkbox.grid(row=3, column=0, padx=20, pady=20)
        #password_placeholder_text = "Password" placeholder_text=password_placeholder_text,
        self.password_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT, state="normal")
        self.password_entry.grid(row=4, column=0, padx=20, pady=20)

        self.joinbutton = customtkinter.CTkButton(master=self.parent, text="Join Room", command=self.create_room,
                                                      hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
        self.joinbutton.grid(row=5, column=0, padx=20, pady=20)
        self.joinbutton.configure(state="disabled")

        self.room_name_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_room_name), "%P"))
        self.room_port_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_room_port), "%P"))
        self.password_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_password), "%P"))
        self.password_entry.insert(0, self.generate_password())


    def toggle_password_entry(self):
        if self.password_checkbox_var.get():
            self.password_entry.configure(state="normal")
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.grid()
            self.password_entry.insert(0, self.generate_password())
        else:
            self.password_entry.pack()
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.configure(state="readonly")


    def generate_password(self):
        password_length = 3
        password_characters = string.ascii_letters + string.digits
        return ''.join(random.choice(password_characters) for _ in range(password_length))
    #generate_password(self)
    def validate_room_name(self, name):
        if len(name) < 2:
            self.joinbutton.configure(state="disabled")
            return True
        elif len(name) > 12:
            truncated_name = name[:12]
            self.room_name_entry.delete(12, "end")
            return False
        else:
            self.joinbutton.configure(state="normal")
            return True
    
    def validate_room_port(self, port):
        if len(port) <= 5:  # Если длина порта меньше или равна 5 символам
            return True     # Пропускаем проверку, так как порт уже установлен и состоит из 5 символов
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
def error_sound():
    threading.Thread(target=play_sound, args=(1000, 500)).start()

def play_sound(frequency, duration):
    winsound.Beep(frequency, duration)

NightTrain = os.path.join(script_dir, "NightTrain.json")
NeonBanana = os.path.join(script_dir, "NeonBanana.json")
customtkinter.set_ctk_parent_class(tkinterDnD.Tk)
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


if not os.path.exists(save_file):
    username = "user" + str(random.randint(0, 9999))
    with open(save_file, "w") as file:
        yaml.dump({"username": username}, file)  # Use yaml.dump to write YAML data
else:
    with open(save_file, "r") as file:
        data = yaml.safe_load(file)  # Use yaml.safe_load to load YAML data
        username = data.get("username", "")

# Load current theme from YAML file if available
current_theme = None
if os.path.exists(save_file):
    with open(save_file, "r") as file:
        data = yaml.safe_load(file)
        current_theme = data.get("theme")

if current_theme is None:
    current_theme = "NightTrain"  # Set default theme if not loaded from YAML
    logging.info('Theme set to NightTrain')
    customtkinter.set_default_color_theme(NightTrain)
elif current_theme == "NightTrain":
    customtkinter.set_default_color_theme(NightTrain)
elif current_theme == "NeonBanana":
    customtkinter.set_default_color_theme(NeonBanana)
else:
    logging.warning("Unknown theme in data.yaml:", current_theme)
def change_theme():
    global current_theme

    if current_theme == "NightTrain":
        current_theme = "NeonBanana"
        logging.info('Theme set to NeonBanana')
        customtkinter.set_default_color_theme(NeonBanana)
    elif current_theme == "NeonBanana":
        current_theme = "NightTrain"
        logging.info('Theme set to NightTrain')
        customtkinter.set_default_color_theme(NightTrain)
    else:
        print("Unknown theme:", current_theme)

    # Load existing data from YAML file
    with open(save_file, "r") as file:
        data = yaml.safe_load(file)

    # Update the theme in the loaded data
    data["theme"] = current_theme

    # Save the updated data back to YAML file
    with open(save_file, "w") as file:
        yaml.dump(data, file)

    os.execv(sys.executable, [sys.executable] + sys.argv)
    app.destroy()

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

import yaml,sys  # Добавим импорт модуля yaml

import yaml
import os
import customtkinter

changeTButton = customtkinter.CTkButton(app, text="Change theme", command=change_theme, hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
changeTButton.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="w")

createRoomButton = customtkinter.CTkButton(app, text="Create room", command=create_room, hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
createRoomButton.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")

info_frame = customtkinter.CTkFrame(master=app,fg_color="transparent")
info_frame.grid(row=0 , column=1, padx=20, pady=(20, 20), sticky="e")

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



def check_internet_connection():
    try:
        # Пытаемся установить соединение с DNS-серверами Google с более коротким временем ожидания
        socket.create_connection(("8.8.8.8", 53), timeout=1)  # Устанавливаем таймаут в 1 секунду
        return True
    except OSError:
        return False

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

