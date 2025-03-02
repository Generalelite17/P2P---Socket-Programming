# P2P Chat Application

A distributed peer-to-peer (P2P) chat application implemented in Python using socket programming. This project demonstrates direct peer connections using a simple, JSON-based protocol for sending chat messages and handling user presence. The application features a graphical user interface (GUI) built with Tkinter for manual connection and messaging.

## Overview

The P2P Chat Application includes:

- **Communication Protocol:**  
  Uses TCP sockets for direct communication between peers. Messages are serialized using JSON and include details such as sender, content, and a timestamp.

- **Manual Peer Connection:**  
  Users manually input their local connection details (Your IP, Your Port, and Username) and also the target peer’s IP and Port to send messages.

- **User Presence:**  
  The `UserPresence` class generates JSON messages indicating online/offline status. These messages are printed/logged as part of the connection process.  
  *(Future Improvement: A dedicated online users list in the GUI.)*

- **Chat Functionality:**  
  Users can send and receive text messages. All messages are displayed in a scrollable chat window along with sender information and timestamps.

- **Concurrency:**  
  The application uses multithreading to handle incoming connections and real-time message updates.


## Project Structure
```bash
P2P-Chat-Application/
├── peer.py                      # Core Peer class for managing TCP connections and message routing
├── message.py                   # Helper functions for creating and parsing JSON messages
├── user_presence.py             # Manages user presence (online/offline) and generates corresponding JSON messages
├── gui.py                       # GUI for manual peer connection and messaging
├── gui_dht.py                   # (Optional) GUI incorporating DHT-based peer discovery
├── README.md                    # Project overview and documentation
├── requirements.txt             # List of dependencies (uses Python standard libraries)
└── LICENSE                      # License file (e.g., MIT License)
```

## Requirements

- Python 3.x (tested on Python 3.13)
- Standard Python libraries: `socket`, `threading`, `json`, `time`, `tkinter`

No additional external packages are required.

## Usage

### Running the GUI Version (Manual Connection)

1. **Launch the GUI:**
   - Open your terminal(main) or command prompt(gui).
   - Navigate to your project directory.
   - Run the command:
     ```bash
     py main.py
     ```
     or
     ```bash
     py gui.py
     ```

2. **Enter Your Connection Details:**
   - **Your IP:** Enter your IP address (e.g., `127.0.0.1`).
   - **Your Port:** Enter a unique port number for your instance (e.g., `5555`).
   - **Username:** Enter your desired username.
   - Click the **Connect** button.

3. **Enter Target Peer Details:**
   - In the chat window (displayed after connecting), enter the **Target IP** and **Target Port** for the peer you wish to message.

4. **Send a Message:**
   - Type your message in the input field.
   - Click the **Send** button.
   - Sent messages and any responses will appear in the chat display area.

### Running Multiple Instances
For testing on the same machine:
- Use your LAN IP (e.g., `127.0.0.1`) for "Your IP."
- Ensure each instance uses a unique local port (e.g., one instance on `5555` and another on `5556`).
- Manually input the target peer’s IP and port for establishing connections.

## Implementation Details

- **Peer Class (peer.py):**  
  Handles setting up a TCP server to listen for incoming connections, message routing, and integrating user presence messages using JSON. It uses multithreading to manage concurrent connections.

- **Message Handling (message.py):**  
  Provides functions to create (`create_message`) and parse (`parse_message`) JSON-formatted messages.

- **User Presence (user_presence.py):**  
  Manages online/offline status of users and generates corresponding JSON messages for propagation.

- **GUI (gui.py):**  
  Implements a Tkinter-based interface for manual peer connection and messaging. Users input their connection details and the target peer's details directly.

- **Optional DHT GUI (gui_dht.py):**  
  A separate version of the GUI (if implemented) that incorporates DHT-based automatic peer discovery.

## Future Improvements

- **Automatic Peer Discovery:**  
  Integrate a Distributed Hash Table (DHT) mechanism for automatic peer discovery instead of manual input.
  
- **Enhanced User Presence Display:**  
  Implement a dedicated section in the GUI to show a list of online users based on presence messages.
  
- **Improved Error Handling and UI Enhancements:**  
  Add more robust error handling and refine the user interface for a better user experience.

## License

This project is licensed under the [MIT License](LICENSE).

