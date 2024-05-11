import os
import random
import customtkinter
import tkinter.messagebox as messagebox
from datetime import datetime
from tkinter import PhotoImage
from PIL import ImageTk, Image
import json
import logging
import socket
import threading
import time


logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s :  %(message)s')

script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, "pc.ico")
icon_pil = Image.open(icon_path)

class CreateRoomWindow:
    def __init__(self, parent):
        logging.info('Creating CreateRoomWindow')

        self.parent = parent
        self.room_name_entry = customtkinter.CTkEntry(master=self.parent)
        self.room_name_entry.grid(row=1, column=0, padx=20, pady=20)

        self.name_length = customtkinter.CTkLabel(master=self.parent, text="Minimum 2 symbols", fg_color="transparent",
                                                  font=("Helvetica", 15, "bold"))
        self.name_length.grid(row=1, column=1, padx=20, pady=20, sticky="w")

        self.room_port_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT)
        self.room_port_entry.grid(row=2, column=0, padx=20, pady=20)

        self.port_length = customtkinter.CTkLabel(master=self.parent, text="Port 1-65535", fg_color="transparent",
                                                  font=("Helvetica", 15, "bold"))
        self.port_length.grid(row=2, column=1, padx=20, pady=20, sticky="w")

        self.password_checkbox_var = customtkinter.BooleanVar(value=True)
        self.password_checkbox = customtkinter.CTkCheckBox(master=self.parent, text="Use Password",
                                                            variable=self.password_checkbox_var,
                                                            command=self.toggle_password_entry)

        self.password_checkbox.grid(row=3, column=0, padx=20, pady=20)
        self.password_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT, state="normal")
        self.password_entry.grid(row=3, column=1, padx=20, pady=20)

        self.create_button = customtkinter.CTkButton(master=self.parent, text="Create Room", command=self.create_room,
                                                     hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
        self.create_button.grid(row=5, column=0, padx=20, pady=20)
        self.create_button.configure(state="disabled")

        self.room_name_entry.configure(validate="key",
                                       validatecommand=(self.parent.register(self.validate_room_name), "%P"))
        self.room_port_entry.configure(validate="key",
                                       validatecommand=(self.parent.register(self.validate_room_port), "%P"))
        self.password_entry.configure(validate="key",
                                      validatecommand=(self.parent.register(self.validate_password), "%P"))

    def toggle_password_entry(self):
        if self.password_checkbox_var.get():
            self.password_entry.configure(state="normal")
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.grid()
        else:
            self.password_entry.grid_remove()
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.configure(state="readonly")

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
        room_port = int(self.room_port_entry.get())
        password = None

        if self.password_checkbox_var.get():
            password = self.password_entry.get()
            if not self.validate_password(password):
                messagebox.showerror("Invalid Password", "Please enter a valid password.")
                return
        сhat_window = ChatAppWindow(self.parent, is_host=True, room_port=room_port, room_password=password)
        self.parent.destroy()
        print("Room Name:", room_name)
        print("Room Port:", room_port)
        if password:
            print("Room Password:", password)

        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", room_port))
                s.listen(1)

                print(f"Room created successfully on port {room_port}!")
                print("Waiting for someone to join...")

                
                conn, addr = s.accept()
                print(f"Connected by {addr}")

                
                if password:
                    
                    received_password = conn.recv(1024).decode()
                    if received_password == password:
                        print("Password accepted. Access granted to the room!")
                        
                        conn.sendall("Access Granted".encode())
                    else:
                        print("Invalid password. Access denied.")
                        
                        conn.sendall("Access Denied".encode())
                        
                        conn.close()
                else:
                    
                    print("No password required. Access granted to the room!")
                    
                    conn.sendall("Access Granted".encode())
            except OSError:
                print("Failed to create the room. Port may be already in use.")
                messagebox.showerror("Room Creation Failed", "Failed to create the room. Port may be already in use.")

class JoinRoomWindow:
    def __init__(self, parent):
        logging.info('Creating JoinRoomWindow')

        self.parent = parent
        self.room_port_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT)
        self.room_port_entry.grid(row=2, column=0, padx=20, pady=20)

        self.port_length = customtkinter.CTkLabel(master=self.parent, text="Port 1-65535", fg_color="transparent",
                                                  font=("Helvetica", 15, "bold"))
        self.port_length.grid(row=2, column=1, padx=20, pady=20, sticky="w")

        self.password_checkbox_var = customtkinter.BooleanVar(value=True)
        self.password_checkbox = customtkinter.CTkCheckBox(master=self.parent, text="Use Password",
                                                            variable=self.password_checkbox_var,
                                                            command=self.toggle_password_entry)

        self.password_checkbox.grid(row=3, column=0, padx=20, pady=20)
        self.password_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT, state="normal")
        self.password_entry.grid(row=4, column=0, padx=20, pady=20)

        self.join_button = customtkinter.CTkButton(master=self.parent, text="Join Room", command=self.join_room,
                                                   hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
        self.join_button.grid(row=5, column=0, padx=20, pady=20)
        self.join_button.configure(state="disabled")

        self.password_entry.configure(validate="key",
                                      validatecommand=(self.parent.register(self.validate_password), "%P"))

    def toggle_password_entry(self):
        if self.password_checkbox_var.get():
            self.password_entry.configure(state="normal")
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.grid()
        else:
            self.password_entry.grid_remove()
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.configure(state="readonly")

    def validate_password(self, password):
        if len(password) > 12:
            password = password[:12]
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.insert(0, password)
            return True
        else:
            return True

    def join_room(self):
        room_ip_port = "localhost:" + self.room_port_entry.get()
        room_password = self.password_entry.get() if self.password_checkbox_var.get() else None

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                room_ip, room_port = room_ip_port.split(":")
                room_port = int(room_port)
                s.connect((room_ip, room_port))
                print("Connected to the room successfully!")
                chat_window = ChatAppWindow(self.parent, is_host=False, room_port=room_port, room_password=password)
                self.parent.destroy()

                if room_password:
                    s.sendall(room_password.encode())
                    response = s.recv(1024).decode()
                    if response == "Access Granted":
                        print("Password accepted. Access granted to the room!")
                    else:
                        print("Invalid password. Access denied.")

                        messagebox.showerror("Invalid Password", "Incorrect password. Please try again.")
                else:
                    print("No password required. Access granted to the room!")
        except (socket.timeout, ConnectionRefusedError):
            print("Connection to the room failed. Please check the IP and port.")
            messagebox.showerror("Connection Failed", "Failed to connect to the room. Please check the IP and port.")



def create_room():
    create_room_window = customtkinter.CTk()
    create_room_window.geometry("380x340")
    create_room_window.title("Create Room")
    CreateRoomWindow(create_room_window)
    create_room_window.mainloop()

def create_join_room():
    join_room_window = customtkinter.CTk()
    join_room_window.geometry("380x340")
    join_room_window.title("Join Room")
    JoinRoomWindow(join_room_window)
    join_room_window.mainloop()

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

NightTrain = os.path.join(script_dir, "NightTrain.json")
current_theme = "NightTrain"
NeonBanana = os.path.join(script_dir, "NeonBanana.json")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme(NightTrain)

save_file = os.path.join(script_dir, "data.json")

def update_username(event=None):
    global username
    new_username = label_1.get()
    if len(new_username) < 1:
        messagebox.showinfo("Error", "Username must contain at least 1 character")
        label_1.configure(fg_color="#c94040")
        label_1.delete(0, customtkinter.END)
        new_username = "user" + str(random.randint(0, 9999))
        label_1.insert(0, new_username)
        update_username()
    else:
        label_1.configure(fg_color="black")
        username = new_username
        with open(save_file, "w") as file:
            json.dump({"username": new_username}, file)

if not os.path.exists(save_file):
    username = "user" + str(random.randint(0, 9999))
    with open(save_file, "w") as file:
        json.dump({"username": username}, file)
else:
    with open(save_file, "r") as file:
        data = json.load(file)
        username = data.get("username", "")

app = customtkinter.CTk()
app.geometry("400x260")
app.title("PythonChat")

label_1 = customtkinter.CTkEntry(master=app, justify=customtkinter.LEFT)
label_1.pack(pady=1)
label_1.grid(row=0, column=0, padx=20, pady=20)

label_1.insert(0, username)

label_1.bind("<KeyRelease>", update_username)

join_room_button = customtkinter.CTkButton(app, text="Join room", command=create_join_room, hover_color="#1b1e48",
                                           font=("Helvetica", 15, "bold"))
join_room_button.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

change_theme_button = customtkinter.CTkButton(app, text="Change theme", command=change_theme, hover_color="#1b1e48",
                                              font=("Helvetica", 15, "bold"))
change_theme_button.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="w")

create_room_button = customtkinter.CTkButton(app, text="Create room", command=create_room, hover_color="#1b1e48",
                                             font=("Helvetica", 15, "bold"))
create_room_button.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")

info_frame = customtkinter.CTkFrame(master=app, fg_color="transparent")
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

def check_internet_periodically():
    while True:
        if check_internet_connection(1):
            internet_status = "Yes"
        else:
            internet_status = "No"

        app.title(f"PythonChat (Connection: {internet_status})")

        time.sleep(1)

def check_internet_connection(timeout):
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False

internet_thread = threading.Thread(target=check_internet_periodically)
internet_thread.daemon = True
internet_thread.start()

icon = ImageTk.PhotoImage(icon_pil)
app.iconphoto(True, icon)
app.minsize(400, 260)
app.maxsize(400, 260)
app.mainloop()
