import json

class UserPresence:
    def __init__(self):
        # Dictionary to store user presence information
        # Format: {username: {"ip": ip_address, "port": port_number}}
        self.presence = {}

    def mark_online(self, username, ip, port):
        """
        Mark a user as online.
        This method updates the presence dictionary and returns a JSON-formatted message
        indicating the user is now online.
        """
        self.presence[username] = {"ip": ip, "port": port}
        # Create a JSON message to propagate this update
        presence_msg = {
            "type": "user_presence",
            "action": "online",
            "username": username,
            "ip": ip,
            "port": port
        }
        return json.dumps(presence_msg)

    def mark_offline(self, username):
        """
        Mark a user as offline.
        Removes the user from the presence dictionary and returns a JSON-formatted message
        indicating the user is now offline.
        """
        if username in self.presence:
            del self.presence[username]
        presence_msg = {
            "type": "user_presence",
            "action": "offline",
            "username": username
        }
        return json.dumps(presence_msg)

    def get_presence_list(self):
        """
        Get the current list of online users.
        Returns a JSON-formatted message containing all online user information.
        """
        presence_list_msg = {
            "type": "presence_list",
            "users": self.presence
        }
        return json.dumps(presence_list_msg)

# Example usage:
if __name__ == "__main__":
    # Create an instance of UserPresence
    up = UserPresence()
    
    # Mark a couple of users as online
    online_msg1 = up.mark_online("Alice", "192.168.1.2", 5001)
    online_msg2 = up.mark_online("Bob", "192.168.1.3", 5002)
    print("Presence update (online):", online_msg1)
    print("Presence update (online):", online_msg2)
    
    # Print the full presence list
    print("Current presence list:", up.get_presence_list())
    
    # Mark one user as offline
    offline_msg = up.mark_offline("Alice")
    print("Presence update (offline):", offline_msg)
    
    # Print the updated presence list
    print("Updated presence list:", up.get_presence_list())
