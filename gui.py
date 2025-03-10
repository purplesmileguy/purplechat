import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
from network import ChatServer, ChatRoomClient
from utils import initialize_config, load_theme, change_theme, error_sound, flash_window
from config import icon_path, save_file
from pyngrok import ngrok
import subprocess
import time
from datetime import datetime
import random
import yaml
class CreateRoomWindow:
    def __init__(self, parent):
        self.parent = parent
        self.room_name_entry = ctk.CTkEntry(master=self.parent, placeholder_text="Room name")
        self.room_name_entry.grid(row=1, column=0, padx=20, pady=20)
        self.room_port_entry = ctk.CTkEntry(master=self.parent, placeholder_text="Port", justify=ctk.LEFT)
        self.room_port_entry.grid(row=2, column=0, padx=20, pady=20)
        self.create_button = ctk.CTkButton(master=self.parent, text="Create Room", command=self.create_room)
        self.create_button.grid(row=5, column=0, padx=20, pady=20)

    def create_room(self):
        room_name = self.room_name_entry.get()
        room_port = self.room_port_entry.get()
        if not room_name or not room_port.isdigit():
            messagebox.showerror("Ошибка", "Введите корректные данные.")
            return
        server = ChatServer(port=int(room_port))
        threading.Thread(target=server.run, daemon=True).start()
        self.start_ngrok(room_port)
        chat_room_window = ctk.CTk()
        chat_room_window.geometry("580x540")
        chat_room_window.title("Chat Room - " + room_name)
        ChatRoomClient(chat_room_window, '127.0.0.1', int(room_port))
        chat_room_window.mainloop()

    def start_ngrok(self, room_port):
        def run_ngrok():
            try:
                tcp_tunnel = ngrok.connect(room_port, "tcp")
                ngrok_url = tcp_tunnel.public_url
                print("ngrok URL:", ngrok_url)
            except Exception as e:
                print("Error starting ngrok:", e)
        threading.Thread(target=run_ngrok).start()

class JoinRoomWindow:
    def __init__(self, parent):
        self.parent = parent
        self.room_url_entry = ctk.CTkEntry(master=self.parent, placeholder_text="Room URL")
        self.room_url_entry.grid(row=0, column=0, padx=20, pady=20)
        self.join_button = ctk.CTkButton(master=self.parent, text="Join Room", command=self.join_room)
        self.join_button.grid(row=3, column=0, padx=20, pady=20)

    def join_room(self):
        room_url = self.room_url_entry.get()
        print("Room URL:", room_url)
        # Здесь должна быть логика подключения к комнате по URL

class MainWindow:
    def __init__(self, app):
        self.app = app
        self.config = initialize_config()
        self.username = self.config["username"]
        self.label_1 = ctk.CTkEntry(master=self.app, justify=ctk.LEFT)
        self.label_1.insert(0, self.username)
        self.label_1.grid(row=0, column=0, padx=20, pady=20)
        self.label_1.bind("<KeyRelease>", self.update_username)
        ctk.CTkButton(self.app, text="Create room", command=self.create_room).grid(row=1, column=0, padx=20, pady=20)
        ctk.CTkButton(self.app, text="Join room", command=self.join_room).grid(row=2, column=0, padx=20, pady=20)
        ctk.CTkButton(self.app, text="Change theme", command=change_theme).grid(row=3, column=0, padx=20, pady=20)
        self.time_label = ctk.CTkLabel(master=self.app, text="", font=("Helvetica", 14))
        self.time_label.grid(row=4, column=0, padx=20, pady=20)
        self.update_time_and_date()

    def update_username(self, event=None):
        new_username = self.label_1.get()
        if len(new_username) < 1:
            messagebox.showinfo("Error", "Username must contain at least 1 character")
            self.label_1.delete(0, tk.END)
            new_username = "user" + str(random.randint(0, 9999))
            self.label_1.insert(0, new_username)
            return
        self.config["username"] = new_username
        with open(save_file, "w") as file:
            yaml.dump(self.config, file)

    def create_room(self):
        create_room_window = ctk.CTk()
        create_room_window.geometry("380x340")
        create_room_window.title("Create Room")
        CreateRoomWindow(create_room_window)
        create_room_window.mainloop()

    def join_room(self):
        join_room_window = ctk.CTk()
        join_room_window.geometry("380x340")
        join_room_window.title("Join Room")
        JoinRoomWindow(join_room_window)
        join_room_window.mainloop()

    def update_time_and_date(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.time_label.configure(text="Time: " + current_time)
        self.app.after(1000, self.update_time_and_date)