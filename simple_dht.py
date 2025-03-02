import socket
import threading
import json
import time

class SimpleDHT:
    def __init__(self, local_host, local_port, username, broadcast_port = 50000, bootstrap_host=None, bootstrap_port=None):
        self.local_host = local_host
        self.local_port = local_port
        self.username = username
        self.broadcast_port = broadcast_port
        self.bootstrap_host = bootstrap_host
        self.bootstrap_port = bootstrap_port
        # Dictionary to store discovered peers: {username: (host, port)}
        self.peers = {}
        # Create a UDP socket for broadcasts
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Allow multiple apps to use the same port (for multicast/broadcast)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.local_port))
        threading.Thread(target=self.listen_for_broadcasts, daemon=True).start()
    
    def broadcast_presence(self):
        """Broadcast this peer's information periodically."""
        message = json.dumps({
            "type": "presence",
            "username": self.username,
            "host": self.local_host,
            "port": self.local_port,
            "timestamp": time.time()
        })
        # Using broadcast address 255.255.255.255 on a specific port, for example 50000
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.sendto(message.encode(), ('192.168.0.255', self.broadcast_port))
    
    def listen_for_broadcasts(self):
        """Listen for incoming presence broadcasts and update peer list."""
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = json.loads(data.decode())
                if message.get("type") == "presence":
                    username = message.get("username")
                    host = message.get("host")
                    port = message.get("port")
                    # Update the peer list if not self
                    if username != self.username:
                        self.peers[username] = (host, port)
                        print(f"Discovered peer: {username} at {host}:{port}")
            except Exception as e:
                print(f"Error in DHT listener: {e}")
    
    def start_broadcasting(self, interval=5):
        """Continuously broadcast presence every few seconds."""
        def run():
            while True:
                self.broadcast_presence()
                time.sleep(interval)
        threading.Thread(target=run, daemon=True).start()
    
    def get_peer_list(self):
        """Return a list of discovered peers."""
        return self.peers

# Example usage:
if __name__ == "__main__":
    dht = SimpleDHT("192.168.0.115", 6000, "Emmanuel", broadcast_port=50000)
    dht.start_broadcasting()
    while True:
        print("Current peers:", dht.get_peer_list())
        time.sleep(10)