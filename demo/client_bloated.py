import socket as sock
from socket import socket as Socket
import pickle, pygame, json, os
import env

# CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

class Client:
    def __init__(self) -> None:
        # with open(CONFIG_PATH, "r") as f:
        #     self.config = json.load(f)
        #     self.IP, self.PORT = self.config["server"]["ip"], self.config["server"]["port"]
        #     self.BUFFER_SIZE, self.HEADER_LENGTH = self.config["client"]["buffer_size"], self.config["server"]["header_length"]
        #     if self.IP == "":
        #         self.IP = sock.gethostname()
        if env.IP == "": env.IP = sock.gethostname()
        self.endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.connect((env.IP, env.PORT))

        self.canvas = pygame.Surface(env.DIMENSIONS)
        self.canvas.fill((20,20,20))

    def listen(self):
        full_message = self.endpoint.recv(env.BUFFER_SIZE)
        is_object = int(chr(full_message[0]))

        message_length = int(full_message[:env.HEADER_LENGTH])

        while len(full_message) - env.HEADER_LENGTH < message_length:
            full_message += self.endpoint.recv(env.BUFFER_SIZE)
        message = full_message[env.HEADER_LENGTH:]

        if not is_object: 
            # prefix of zero if message should be decoded to a string
            print(message.decode("utf-8"))
            return

        # if not self.has_canvas:
        #     self.canvas: pygame.PixelArray = pickle.loads(message)
        #     self.has_canvas = True
        #     return
        
        # otherwise it should be treated as an object
        self.canvas = pickle.loads(message)

    def send(self, point_stack):
        encoded = self.encode_object(point_stack)
        self.endpoint.send(encoded)

    def encode_object(self, point_stack: list):
        pickled = pickle.dumps(point_stack)
        with_header = bytes(f"{len(pickled):<{env.HEADER_LENGTH}}", "utf-8") + pickled
        # return bytes(with_header, "utf-8")
        return with_header