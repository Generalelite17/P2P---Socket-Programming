import tkinter as tk
from tkinter import scrolledtext, messagebox, END
from peer import Peer  # Your Peer class for P2P communication

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("P2P Chat Application")
        self.peer = None

        # ---------------------------
        # Connection Frame
        # ---------------------------
        self.login_frame = tk.Frame(master)
        self.login_frame.pack(padx=10, pady=10)

        # Connection Details
        tk.Label(self.login_frame, text="User Credentials", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(self.login_frame, text="Your IP:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.ip_entry = tk.Entry(self.login_frame, width=15)
        self.ip_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.login_frame, text="Your Port:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.port_entry = tk.Entry(self.login_frame, width=15)
        self.port_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.login_frame, text="Username:").grid(row=3, column=0, sticky="e", padx=5, pady=2)
        self.username_entry = tk.Entry(self.login_frame, width=15)
        self.username_entry.grid(row=3, column=1, padx=5, pady=2)

        self.connect_btn = tk.Button(self.login_frame, text="Connect", command=self.connect)
        self.connect_btn.grid(row=6, column=0, columnspan=2, pady=10)

        # ---------------------------
        # Chat Frame (Hidden initially)
        # ---------------------------
        self.chat_frame = tk.Frame(master)

        # Target Details Frame in the Chat Window
        target_frame = tk.Frame(self.chat_frame)
        target_frame.pack(padx=10, pady=(5, 0), fill="x")
        tk.Label(target_frame, text="Target IP:").pack(side="left", padx=5)
        self.target_ip_entry = tk.Entry(target_frame, width=15)
        self.target_ip_entry.pack(side="left", padx=5)
        tk.Label(target_frame, text="Target Port:").pack(side="left", padx=5)
        self.target_port_entry = tk.Entry(target_frame, width=15)
        self.target_port_entry.pack(side="left", padx=5)

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

    def connect(self):
        # Get connection details from entry fields
        host = self.ip_entry.get().strip()
        port_str = self.port_entry.get().strip()
        username = self.username_entry.get().strip()

        if not host or not port_str or not username:
            messagebox.showerror("Error", "Please fill in your IP, Port, and Username.")
            return

        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Error", "Your port must be a number.")
            return

        # Instantiate the Peer using the GUI callback for incoming messages
        try:
            self.peer = Peer(host, port, username, update_chat_callback=self.update_chat)
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            return

        # Hide the connection frame and show the chat frame
        self.login_frame.pack_forget()
        self.chat_frame.pack(padx=10, pady=10)

    def update_chat(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(END, message + "\n")
        self.chat_display.config(state="disabled")
        self.chat_display.yview(END)

    def send_message(self):
        target_ip = self.target_ip_entry.get().strip()
        target_port_str = self.target_port_entry.get().strip()

        if not target_ip or not target_port_str:
            messagebox.showerror("Error", "Please enter the target IP and port before sending.")
            return

        try:
            target_port = int(target_port_str)
        except ValueError:
            messagebox.showerror("Error", "Target port must be a number.")
            return

        msg = self.msg_entry.get().strip()
        if not msg:
            messagebox.showerror("Error", "Please enter a message to send.")
            return

        if self.peer:
            self.peer.send_message(target_ip, target_port, msg)
            self.update_chat(f"You to {target_ip}:{target_port}: {msg}")
            self.msg_entry.delete(0, END)
        else:
            messagebox.showerror("Error", "You are not connected.")

    def on_close(self):
        if self.peer:
            try:
                self.peer.server_socket.close()
            except Exception:
                pass
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
