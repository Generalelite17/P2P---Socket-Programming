import socket

def receive_broadcast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 50000))
    print("Listening for broadcasts on port 50000...")
    while True:
        data, addr = sock.recvfrom(1024)
        print("Received from {}: {}".format(addr, data.decode()))

if __name__ == "__main__":
    receive_broadcast()
