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
import json
import random
import string
import logging
import ctypes

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

def join_room():
    logging.info('Action: join_room')
    print("button pressed")
    threading.Thread(target=play_sound, args=(1000, 500)).start()

def create_room():
    logging.info('Action: create_room')
    create_room_window = customtkinter.CTk()
    create_room_window.geometry("300x440")
    create_room_window.title("Create Room")
    CreateRoomWindow(create_room_window)
    create_room_window.mainloop()

def create_join_room():
    logging.info('Action: create_join_room')
    join_room_window = customtkinter.CTk()
    join_room_window.geometry("200x440")
    join_room_window.title("Join Room")
    #JoinRoomWindow(join_room_window)
    join_room_window.mainloop()

class CreateRoomWindow:
    def __init__(self, parent):
        logging.info('Creating CreateRoomWindow')
        name_placeholder_text = "Room name"

        self.parent = parent
        self.room_name_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT, placeholder_text=name_placeholder_text)
        self.room_name_entry.grid(row=1, column=0, padx=20, pady=20)
        port_placeholder_text = "Port"
        self.room_port_entry = customtkinter.CTkEntry(master=self.parent, placeholder_text=port_placeholder_text, justify=customtkinter.LEFT)
        self.room_port_entry.grid(row=2, column=0, padx=20, pady=20)
        
        self.password_checkbox_var = customtkinter.BooleanVar(value=True)
        self.password_checkbox = customtkinter.CTkCheckBox(master=self.parent, text="Use Password",
                                                           variable=self.password_checkbox_var,
                                                           command=self.toggle_password_entry)
        self.password_checkbox.grid(row=3, column=0, padx=20, pady=20)
        password_placeholder_text = "Password"
        self.password_entry = customtkinter.CTkEntry(master=self.parent, justify=customtkinter.LEFT, placeholder_text=password_placeholder_text, state="normal")
        self.password_entry.grid(row=4, column=0, padx=20, pady=20)

        self.create_button = customtkinter.CTkButton(master=self.parent, text="Create Room", command=self.create_room,
                                                      hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
        self.create_button.grid(row=5, column=0, padx=20, pady=20)
        self.create_button.configure(state="disabled")

        self.room_name_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_room_name), "%P"))
        self.room_port_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_room_port), "%P"))
        self.password_entry.configure(validate="key", validatecommand=(self.parent.register(self.validate_password), "%P"))
        
    def toggle_password_entry(self):
        if self.password_checkbox_var.get():
            self.password_entry.configure(state="normal")
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.insert(0, self.generate_password())
        else:
            self.password_entry.delete(0, customtkinter.END)
            self.password_entry.configure(state="readonly")

    def generate_password(self):
        password_length = 12
        password_characters = string.ascii_letters + string.digits
        return ''.join(random.choice(password_characters) for _ in range(password_length))

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
        if not port.isdigit():
            return False
        port = int(port)
        if port < 5 or port > 65535:
            messagebox.showerror("Invalid Port", "Port must be between 5 and 65535")
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
current_theme = "NightTrain"
NeonBanana = os.path.join(script_dir, "NeonBanana.json")
customtkinter.set_ctk_parent_class(tkinterDnD.Tk)
customtkinter.deactivate_automatic_dpi_awareness()
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme(NightTrain)

username1 = "user" + str(random.randint(0, 9999))

save_file = "data.json"

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

joinRoomButton = customtkinter.CTkButton(app, text="Join room", command=create_join_room, hover_color="#1b1e48", font=("Helvetica", 15, "bold"))
joinRoomButton.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

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

icon = ImageTk.PhotoImage(icon_pil)
app.iconphoto(True, icon)
app.wm_iconbitmap()
app.minsize(400, 260)
app.maxsize(400, 260)
app.mainloop()
