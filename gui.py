from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QDialog, QLabel, QCheckBox
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIntValidator
from network import ChatServer, ChatRoomClient
from utils import initialize_config, change_theme, error_sound, flash_window
from config import icon_path, save_file
import threading
import subprocess
import time
from datetime import datetime
import random
import yaml

class CreateRoomWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Room")
        self.setGeometry(100, 100, 380, 340)
        layout = QVBoxLayout()

        config = initialize_config()
        self.username = config["username"]
        default_room_name = f"{self.username}_{random.randint(0, 99):02d}"
        self.room_name_entry = QLineEdit(default_room_name, self)
        self.room_name_entry.setPlaceholderText("Room name")
        layout.addWidget(self.room_name_entry)

        self.room_port_entry = QLineEdit("12345", self)
        self.room_port_entry.setPlaceholderText("Port")
        self.room_port_entry.setValidator(QIntValidator(1024, 65535, self))
        layout.addWidget(self.room_port_entry)

        self.password_checkbox = QCheckBox("Enable Password", self)
        self.password_checkbox.stateChanged.connect(self.toggle_password_field)
        layout.addWidget(self.password_checkbox)

        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Password (max 12 chars, no spaces)")
        self.password_entry.setMaxLength(12)
        self.password_entry.setEnabled(False)
        layout.addWidget(self.password_entry)

        self.create_button = QPushButton("Create Room", self)
        self.create_button.clicked.connect(self.create_room)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def toggle_password_field(self, state):
        self.password_entry.setEnabled(state == Qt.CheckState.Checked.value)

    def create_room(self):
        room_name = self.room_name_entry.text()
        room_port = self.room_port_entry.text()
        password = self.password_entry.text() if self.password_checkbox.isChecked() else None

        if not room_name or not room_port:
            error_sound()
            print("Yo, fill in the blanks, dude!")
            return
        if self.password_checkbox.isChecked() and (not password or " " in password):
            error_sound()
            print("Password’s gotta be solid — no spaces, my friend!")
            return

        server = ChatServer(port=int(room_port))
        server.password = password
        threading.Thread(target=server.run, daemon=True).start()
        self.start_serveo(room_port)
        chat_room_window = ChatRoomClient('127.0.0.1', int(room_port), self.username)
        chat_room_window.setWindowTitle("Chat Room - " + room_name)
        self.accept()
        chat_room_window.show()

    def start_serveo(self, room_port):
        def run_serveo():
            try:
                process = subprocess.Popen(
                    ["ssh", "-n", "-o", "StrictHostKeyChecking=no", "-R", f"0:localhost:{room_port}", "serveo.net"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                stdout, stderr = process.communicate()
                if stderr:
                    print(f"Serveo threw a tantrum: {stderr}")
                else:
                    for line in stdout.splitlines():
                        if "Forwarding" in line:
                            public_url = line.split()[-1]
                            print(f"Serveo’s rocking it at: {public_url}")
                            break
            except Exception as e:
                print(f"Serveo crashed the party: {e}")
        threading.Thread(target=run_serveo).start()

class JoinRoomWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Join Room")
        self.setGeometry(100, 100, 380, 340)
        layout = QVBoxLayout()

        config = initialize_config()
        self.username = config["username"]

        self.room_url_entry = QLineEdit("tcp://127.0.0.1:12345", self)
        self.room_url_entry.setPlaceholderText("Room URL (e.g., tcp://host:port)")
        layout.addWidget(self.room_url_entry)

        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Password (if required)")
        self.password_entry.setMaxLength(12)
        layout.addWidget(self.password_entry)

        self.join_button = QPushButton("Join Room", self)
        self.join_button.clicked.connect(self.join_room)
        layout.addWidget(self.join_button)

        self.setLayout(layout)

    def join_room(self):
        room_url = self.room_url_entry.text()
        password = self.password_entry.text()
        if not room_url.startswith("tcp://"):
            error_sound()
            print("URL’s gotta start with tcp://, bro!")
            return
        try:
            host_port = room_url.replace("tcp://", "").split(":")
            server_ip = host_port[0]
            server_port = int(host_port[1])
            chat_room_window = ChatRoomClient(server_ip, server_port, self.username, password=password)
            chat_room_window.show()
            self.accept()
        except (IndexError, ValueError) as e:
            error_sound()
            print(f"Joining crashed: {e}")

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("PythonChat")
        self.setGeometry(100, 100, 400, 260)
        self.config = initialize_config()
        self.username = self.config["username"]

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.label_1 = QLineEdit(self.username)
        self.label_1.setPlaceholderText("Enter your username")
        self.label_1.textChanged.connect(self.update_username)
        layout.addWidget(self.label_1)

        self.create_room_button = QPushButton("Create room")
        self.create_room_button.clicked.connect(self.create_room)
        layout.addWidget(self.create_room_button)

        self.join_room_button = QPushButton("Join room")
        self.join_room_button.clicked.connect(self.join_room)
        layout.addWidget(self.join_room_button)

        self.change_theme_button = QPushButton("Change theme")
        self.change_theme_button.clicked.connect(lambda: change_theme(self.app))
        layout.addWidget(self.change_theme_button)

        self.time_label = QLabel("Time: ")
        layout.addWidget(self.time_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_and_date)
        self.timer.start(1000)

    def update_username(self):
        new_username = self.label_1.text()
        if len(new_username) < 1:
            error_sound()
            self.label_1.setText("user" + str(random.randint(0, 9999)))
            print("Username can’t be empty, dude!")
            return
        self.config["username"] = new_username
        with open(save_file, "w") as file:
            yaml.dump(self.config, file)

    def create_room(self):
        dialog = CreateRoomWindow(self)
        dialog.exec()

    def join_room(self):
        dialog = JoinRoomWindow(self)
        dialog.exec()

    def update_time_and_date(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.time_label.setText(f"Time: {current_time}")