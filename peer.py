import socket
import threading
import json
import time
from message import create_message, parse_message
from user_presence import UserPresence

class Peer:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.user_presence = UserPresence()  # Manage presence info
        self.peers = {}  # Could store known peers, e.g., {username: (ip, port)}
        
        # Set up the server to listen for incoming connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[{self.username}] Listening on {self.host}:{self.port}")
        
        # Start the thread that accepts incoming connections
        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Mark yourself as online (could also propagate this to other peers)
        print(self.user_presence.mark_online(self.username, self.host, self.port))

    def accept_connections(self):
        """ Continuously accepts incoming connections and spawns a thread to handle each. """
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"[{self.username}] Connection established with {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        """ Receives and processes messages from a connected peer. """
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                data = parse_message(message)
                sender = data.get('sender')
                content = data.get('content')
                timestamp = data.get('timestamp')
                print(f"[{self.username}] Received from {sender} at {time.ctime(timestamp)}: {content}")
                
                # Optionally, send back an acknowledgment
                ack = create_message(self.username, "Ack: Message received")
                client_socket.send(ack.encode())
            except Exception as e:
                print(f"[{self.username}] Error handling message: {e}")
                break
        client_socket.close()

    def send_message(self, target_host, target_port, content):
        """ Connects to a target peer and sends a formatted message. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((target_host, target_port))
                msg = create_message(self.username, content)
                client_socket.send(msg.encode())
                
                # Optionally wait for an acknowledgment
                ack = client_socket.recv(1024).decode()
                if ack:
                    print(f"[{self.username}] Received ack: {parse_message(ack)['content']}")
        except Exception as e:
            print(f"[{self.username}] Error sending message: {e}")
