import socket as sock
from socket import socket as Socket
import pickle, pygame, json, os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

class Client:
    def __init__(self) -> None:
        with open(CONFIG_PATH, "r") as f:
            self.config = json.load(f)
            self.IP, self.PORT = self.config["server"]["ip"], self.config["server"]["port"]
            self.BUFFER_SIZE, self.HEADER_LENGTH = self.config["client"]["buffer_size"], self.config["server"]["header_length"]
            if self.IP == "":
                self.IP = sock.gethostname()
        self.endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.connect((self.IP, self.PORT))

        self.has_canvas = False

        self.point_stack = [] # List of coordinates not yet drawn to the canvas

    def listen(self):
        full_message = self.endpoint.recv(self.BUFFER_SIZE)
        is_object = int(chr(full_message[0]))

        message_length = int(full_message[:self.HEADER_LENGTH])

        while len(full_message) - self.HEADER_LENGTH < message_length:
            full_message += self.endpoint.recv(self.BUFFER_SIZE)
        message = full_message[self.HEADER_LENGTH:]

        if not is_object: 
            # prefix of zero if message should be decoded to a string
            print(message.decode("utf-8"))
            return

        if not self.has_canvas:
            self.canvas: pygame.PixelArray = pickle.loads(message)
            self.has_canvas = True
            return
        
        # otherwise it should be treated as an object
        self.point_stack.append(pickle.loads(message))