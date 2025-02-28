import json
import time

def create_message(sender, content):
    """ Create a structured message (JSON format). """
    message = {
        'sender': sender,
        'content': content,
        'timestamp': time.time()  # add timestamp for message order
    }
    return json.dumps(message)

def parse_message(message_json):
    """ Parse received JSON message. """
    return json.loads(message_json)
