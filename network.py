import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
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