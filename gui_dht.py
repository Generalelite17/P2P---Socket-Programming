import tkinter as tk
from tkinter import scrolledtext, messagebox
from peer import Peer  # Your Peer class for P2P communication

class ChatGUI:
    def __init__(self, master, dht):
        self.master = master
        self.dht = dht  # Instance of your discovery module
        master.title("P2P Chat Application")
        self.peer = None

        # ---------------------------
        # Login (Connection) Frame
        # ---------------------------
        self.login_frame = tk.Frame(master)
        self.login_frame.pack(padx=10, pady=10)

        tk.Label(self.login_frame, text="User Credentials", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(self.login_frame, text="Your IP:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Label(self.login_frame, text="Your Port:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        #tk.Label(self.login_frame, text="Broadcast Port:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        tk.Label(self.login_frame, text="Username:").grid(row=4, column=0, sticky="e", padx=5, pady=5)

        self.ip_entry = tk.Entry(self.login_frame)
        self.port_entry = tk.Entry(self.login_frame)
        #self.broadcast_port_entry = tk.Entry(self.login_frame)
        self.username_entry = tk.Entry(self.login_frame)
        self.ip_entry.grid(row=1, column=1, padx=5, pady=5)
        self.port_entry.grid(row=2, column=1, padx=5, pady=5)
        #self.broadcast_port_entry.grid(row=3, column=1, padx=5, pady=5)
        self.username_entry.grid(row=4, column=1, padx=5, pady=5)

        self.connect_btn = tk.Button(self.login_frame, text="Connect", command=self.connect)
        self.connect_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # ---------------------------
        # Chat Frame (Hidden initially)
        # ---------------------------
        self.chat_frame = tk.Frame(master)

        # Chat Display Area
        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, width=60, height=20, state="disabled", wrap="word")
        self.chat_display.pack(padx=10, pady=5)

        # Message Input Area
        self.msg_frame = tk.Frame(self.chat_frame)
        self.msg_frame.pack(padx=10, pady=5, fill="x")

        self.msg_entry = tk.Entry(self.msg_frame, width=40)
        self.msg_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        self.send_btn = tk.Button(self.msg_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side="left", padx=5, pady=5)

        # Target Peer Details using a scrollable Listbox for discovered peers
        self.peer_list_frame = tk.Frame(self.chat_frame)
        self.peer_list_frame.pack(padx=10, pady=5, fill="both", expand=True)

        tk.Label(self.peer_list_frame, text="Online Devices:").pack(anchor="w", padx=5, pady=5)

        # Create a Listbox with a vertical scrollbar
        self.peer_listbox = tk.Listbox(self.peer_list_frame, height=6)
        self.peer_listbox.pack(side="left", fill="both", expand=True, padx=(5,0), pady=5)
        self.scrollbar = tk.Scrollbar(self.peer_list_frame, orient="vertical", command=self.peer_listbox.yview)
        self.scrollbar.pack(side="right", fill="y", padx=(0,5), pady=5)
        self.peer_listbox.config(yscrollcommand=self.scrollbar.set)

        # Button to refresh the peer list manually
        self.refresh_btn = tk.Button(self.chat_frame, text="Refresh Devices", command=self.refresh_peer_list)
        self.refresh_btn.pack(padx=10, pady=5)

        # Automatically refresh the peer list every 5 seconds
        self.master.after(5000, self.refresh_peer_list)

    def connect(self):
        # Get login details from entry fields
        host = self.ip_entry.get().strip()  # Using host for consistency
        port_str = self.port_entry.get().strip()
        #broadcast_port_str = self.broadcast_port_entry.get().strip()
        username = self.username_entry.get().strip()

        if not host or not port_str or not "broadcast_port_str" or not username:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            port = int(port_str)
            #broadcast_port = int(broadcast_port_str)
        except ValueError:
            messagebox.showerror("Error", "Port and broadcast port must be numbers.")
            return

        # Instantiate the Peer with the GUI callback for incoming messages
        try:
            self.peer = Peer(host, port, username, update_chat_callback=self.update_chat)
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            return

        # Start the discovery module using the provided broadcast port
        try:
            #self.dht.local_port = broadcast_port  # Update DHT to use the user-specified broadcast port
            self.dht.start_broadcasting()
        except Exception as e:
            messagebox.showerror("DHT Error", str(e))
            return

        # Hide login frame and show chat frame
        self.login_frame.pack_forget()
        self.chat_frame.pack(padx=10, pady=10)

    def refresh_peer_list(self):
        # Get the discovered peers from the DHT module (e.g., {'Emma': ('127.0.0.1', 5556), ...})
        peers = self.dht.get_peer_list()
        # Clear the listbox and insert updated peer names
        self.peer_listbox.delete(0, tk.END)
        for username, (ip, port) in peers.items():
            self.peer_listbox.insert(tk.END, f"{username}: {ip}:{port}")
        # Reschedule the refresh
        self.master.after(5000, self.refresh_peer_list)

    def update_chat(self, message):
        # Append new messages to the chat display area
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state="disabled")
        self.chat_display.yview(tk.END)

    def send_message(self):
        target_ip = self.peer_listbox.get(tk.ACTIVE)
        # Expect target format: "username: ip:port". Parse to extract ip and port.
        try:
            _, target_info = target_ip.split(":", 1)
            target_ip, target_port = target_info.strip().split(":")
            target_port = int(target_port)
        except Exception as e:
            messagebox.showerror("Error", "Please select a valid target device from the list.")
            return

        msg = self.msg_entry.get().strip()

        if not msg:
            messagebox.showerror("Error", "Please enter a message to send.")
            return

        if self.peer:
            self.peer.send_message(target_ip, target_port, msg)
            self.update_chat(f"You to {target_ip}:{target_port}: {msg}")
            self.msg_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "You are not connected.")

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    # Import your discovery module (e.g., SimpleDHT)
    from simple_dht import SimpleDHT  # Ensure your discovery code is in simple_dht.py
    # Create an instance of the DHT for discovery
    # Note: We pass a default port here; it will be updated by the user's input in connect().
    dht = SimpleDHT("127.0.0.1", 6000, "Emmanuel")
    app = ChatGUI(root, dht)
    root.mainloop()
