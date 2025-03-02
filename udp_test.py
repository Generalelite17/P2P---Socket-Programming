import socket

def test_broadcast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = "Test broadcast"
    try:
        sock.sendto(message.encode(), ('192.168.0.255', 50000))
        print("Broadcast sent!")
    except Exception as e:
        print("Error sending broadcast:", e)

if __name__ == "__main__":
    test_broadcast()
