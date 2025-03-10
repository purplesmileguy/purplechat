import socket
import threading
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QApplication
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.client_info = {}
        self.password = None
        self.creator_socket = None
        self.banned_clients = set()

    def handle_client(self, client_socket):
        client_ip = client_socket.getpeername()[0]
        if client_ip in self.banned_clients:
            client_socket.send("You are banned!".encode('utf-8'))
            client_socket.close()
            return

        if client_socket != self.creator_socket and self.password:
            try:
                client_socket.send("Enter password:".encode('utf-8'))
                client_password = client_socket.recv(1024).decode('utf-8').strip()
                if client_password != self.password:
                    client_socket.send("Incorrect password".encode('utf-8'))
                    client_socket.close()
                    print(f"Client {client_socket.getpeername()} kicked — wrong password!")
                    return
                client_socket.send("Password accepted".encode('utf-8'))
            except:
                client_socket.close()
                return

        client_socket.send("Enter your nickname:".encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8').strip()
        self.clients.append(client_socket)
        self.client_info[client_socket] = [nickname, "green"]
        self.broadcast_client_list()

        print(f"Welcome aboard, {nickname} at {client_socket.getpeername()}!")
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                if message.startswith("STATUS:"):
                    status = message.split(":", 1)[1]
                    self.client_info[client_socket][1] = status
                    self.broadcast_client_list()
                elif message == "!banme":
                    self.banned_clients.add(client_ip)
                    client_socket.send("You are banned!".encode('utf-8'))
                    break
                else:
                    print(f"Received message: {message} from {nickname}")
                    self.broadcast(f"{nickname}: {message}", client_socket)
            except ConnectionResetError:
                break
        client_socket.close()
        self.clients.remove(client_socket)
        self.client_info[client_socket][1] = "gray"
        self.broadcast_client_list()
        print(f"Client {nickname} left the party!")

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                    print(f"Broadcasted '{message}' to {client.getpeername()}")
                except:
                    client.close()
                    self.clients.remove(client)
                    self.client_info[client][1] = "gray"
                    self.broadcast_client_list()

    def broadcast_client_list(self):
        client_list = ";".join(f"{info[0]}:{info[1]}" for info in self.client_info.values())
        message = f"CLIENT_LIST:{client_list}"
        for client in self.clients:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                self.clients.remove(client)
                self.client_info[client][1] = "gray"

    def run(self):
        print("Server is rocking the house!")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"New guest at the door: {addr}")
            if not self.creator_socket:
                self.creator_socket = client_socket
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

class ChatRoomClient(QMainWindow):
    message_received = pyqtSignal(str)

    def __init__(self, server_ip, server_port, nickname, password=None):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.nickname = nickname
        self.password = password
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.server_ip, self.server_port))
            print(f"Connected to the party at {server_ip}:{server_port}")
            initial_message = self.socket.recv(1024).decode('utf-8')
            if "Enter password:" in initial_message and self.password:
                self.socket.send(self.password.encode('utf-8'))
                response = self.socket.recv(1024).decode('utf-8')
                if "Incorrect password" in response:
                    raise Exception("Incorrect password — no entry!")
                print("Password accepted — VIP status granted!")
            self.socket.send(nickname.encode('utf-8'))
        except Exception as e:
            print(f"Oops, connection crashed: {e}")
            self.socket.close()
            return
        self.init_ui()
        self.message_received.connect(self.display_message, Qt.ConnectionType.QueuedConnection)
        print("Signal connected — ready to rock the stage!")
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        self.update_status()

    def init_ui(self):
        self.setWindowTitle(f"Chat Room - {self.nickname}")
        self.setGeometry(100, 100, 800, 540)
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()

        self.chat_list = QListWidget()
        layout.addWidget(self.chat_list)

        self.message_entry = QLineEdit()
        layout.addWidget(self.message_entry)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        self.client_list = QListWidget()
        layout.addWidget(self.client_list)

        widget.setLayout(layout)
        self.focusInEvent = self.on_focus_in
        self.focusOutEvent = self.on_focus_out

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Client got a hot message: {message}")
                    self.message_received.emit(message)
                    QApplication.processEvents()
            except Exception as e:
                print(f"Message lost in the void: {e}")
                break

    def display_message(self, message):
        if message.startswith("CLIENT_LIST:"):
            self.update_client_list(message.split(":", 1)[1])
        else:
            print(f"Lighting up the screen with: {message}")
            item = QListWidgetItem(message)
            self.chat_list.addItem(item)
            self.chat_list.scrollToBottom()
            print(f"Added to chat_list: {message}")

    def update_client_list(self, client_list_str):
        self.client_list.clear()
        for client_info in client_list_str.split(";"):
            if ":" in client_info:
                nickname, status = client_info.split(":")
                item = QListWidgetItem(nickname)
                if status == "green":
                    item.setBackground(QColor("green"))
                elif status == "yellow":
                    item.setBackground(QColor("yellow"))
                elif status == "gray":
                    item.setBackground(QColor("gray"))
                elif status == "red":
                    item.setBackground(QColor("red"))
                self.client_list.addItem(item)

    def send_message(self):
        message = self.message_entry.text()
        if message:
            try:
                # Показываем своё сообщение сразу в интерфейсе
                self.display_message(f"{self.nickname}: {message}")
                self.socket.send(message.encode('utf-8'))
                print(f"Sent a banger: {message}")
                self.message_entry.clear()
            except Exception as e:
                print(f"Send failed — mic drop: {e}")

    def update_status(self):
        status = "green" if self.isActiveWindow() else "yellow"
        try:
            self.socket.send(f"STATUS:{status}".encode('utf-8'))
        except:
            pass

    def on_focus_in(self, event):
        self.update_status()

    def on_focus_out(self, event):
        self.update_status()