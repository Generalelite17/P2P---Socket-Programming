import tkinter as tk
from tkinter import scrolledtext, messagebox
from peer import Peer  # Make sure your Peer class is updated to accept update_chat_callback

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("P2P Chat Application")
        self.peer = None

        # ---------------------------
        # Login (Connection) Frame
        # ---------------------------
        self.login_frame = tk.Frame(master)
        self.login_frame.pack(padx=10, pady=10)

        tk.Label(self.login_frame, text="User Credentials", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(self.login_frame, text="Your host:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Label(self.login_frame, text="Your Port:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Label(self.login_frame, text="Username:").grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.host_entry = tk.Entry(self.login_frame)
        self.port_entry = tk.Entry(self.login_frame)
        self.username_entry = tk.Entry(self.login_frame)
        self.host_entry.grid(row=1, column=1, padx=5, pady=5)
        self.port_entry.grid(row=2, column=1, padx=5, pady=5)
        self.username_entry.grid(row=3, column=1, padx=5, pady=5)

        self.connect_btn = tk.Button(self.login_frame, text="Connect", command=self.connect)
        self.connect_btn.grid(row=4, column=0, columnspan=2, pady=10)

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

        # Target Peer Details (stays on chat screen)
        self.target_frame = tk.Frame(self.chat_frame)
        self.target_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(self.target_frame, text="Target host:").pack(side="left", padx=5)
        self.target_host_entry = tk.Entry(self.target_frame, width=15)
        self.target_host_entry.pack(side="left", padx=5)
        tk.Label(self.target_frame, text="Port:").pack(side="left", padx=5)
        self.target_port_entry = tk.Entry(self.target_frame, width=5)
        self.target_port_entry.pack(side="left", padx=5)

    def connect(self):
        # Get login details from entry fields
        host = self.host_entry.get().strip()
        port_str = self.port_entry.get().strip()
        username = self.username_entry.get().strip()

        if not host or not port_str or not username:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Error", "Port must be a number.")
            return

        # Instantiate the Peer with the GUI callback for incoming messages
        try:
            self.peer = Peer(host, port, username, update_chat_callback=self.update_chat)
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            return

        # Hide login frame and show chat frame
        self.login_frame.pack_forget()
        self.chat_frame.pack(padx=10, pady=10)

    def update_chat(self, message):
        # Append new messages to the chat display area
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state="disabled")
        self.chat_display.yview(tk.END)

    def send_message(self):
        target_host = self.target_host_entry.get().strip()
        target_port_str = self.target_port_entry.get().strip()
        msg = self.msg_entry.get().strip()

        if not target_host or not target_port_str or not msg:
            messagebox.showerror("Error", "Please fill in target host, port, and message.")
            return

        try:
            target_port = int(target_port_str)
        except ValueError:
            messagebox.showerror("Error", "Target port must be a number.")
            return

        if self.peer:
            self.peer.send_message(target_host, target_port, msg)
            self.update_chat(f"You to {target_host}:{target_port}: {msg}")
            self.msg_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "You are not connected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()
