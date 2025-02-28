from peer import Peer  # Import the Peer class from peer.py

def main():
    # Gather basic connection details from the user.
    host = input("Enter your IP address (e.g., 127.0.0.1): ")
    port = int(input("Enter your port: "))
    username = input("Enter your username: ")
    
    # Instantiate a Peer object, which sets up the server, user presence, etc.
    peer = Peer(host, port, username)
    
    # Main interactive loop: this is where you call methods from your Peer class.
    while True:
        print("\nCommands:")
        print("1. Send a message")
        print("2. Exit")
        command = input("Enter command: ").strip().lower()
        
        if command in ("1", "send"):
            target_ip = input("Enter target peer IP: ")
            target_port = int(input("Enter target peer port: "))
            message = input("Enter your message: ")
            peer.send_message(target_ip, target_port, message)
        elif command in ("2", "exit"):
            print("Exiting application.")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
