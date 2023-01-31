import socket as sock
from socket import socket as Socket
import threading, sys, time, json, os, pygame, pickle
from typing import Optional
import env
# from config import DIMENSIONS

# CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

class Server:
    def __init__(self) -> None:
        # with open(CONFIG_PATH, "r") as f:
        #     self.config = json.load(f)
        #     self.IP, self.PORT = self.config["server"]["ip"], self.config["server"]["port"]
        #     self.MAX_SOCKETS, self.HEADER_LENGTH = self.config["server"]["max_sockets"], self.config["server"]["header_length"]
        #     if self.IP == "":
        #         self.IP = sock.gethostname()

        if env.IP == "": env.IP = sock.gethostname()
        self.endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
        # # Set the socket option level to reuse the adress
        self.endpoint.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.endpoint.bind((env.IP, env.PORT))
        self.endpoint.listen(env.MAX_SOCKETS)

        print(f"Started server on {env.IP}:{env.PORT}")

        self.client_threads = {}
        self.is_running = True
        self.clock = pygame.time.Clock()

        self.canvas = pygame.Surface(env.DIM)
        self.canvas.fill((20,20,20))
        self.point_stack = []
        
    def accept_clients(self):
        client_endpoint, address = self.endpoint.accept()
        print(f"Connection from {address} has been made.")

        new_thread = threading.Thread(target=self.handle_client, args=(client_endpoint, address))
        new_thread.start()
        self.client_threads[address] = new_thread

        # client_threads = [threading.Thread(target=self.accept_clients) for _ in range(self.MAX_SOCKETS)]
        # TODO: implement threading/async code execution
        # Threading: https://www.youtube.com/watch?v=IEEhzQoKtQU&t=1s 
        # Asyncio: https://www.youtube.com/watch?v=t5Bo1Je9EmE

    def handle_client(self, client_endpoint: Socket, address: tuple):
        welcome_msg = self.to_bytes(f"Joined server {env.IP}:{env.PORT}")
        client_endpoint.send(welcome_msg)

        while self.is_running:

            listening_thread = threading.Thread(target=self.recieve_messages, args=(client_endpoint, address))
            listening_thread.start()

            print("new listen")

            for i in reversed(range(len(self.point_stack))):
                point = self.point_stack.pop(i)
                print(point)
                pygame.draw.circle(self.canvas, point["c"], point["p"], point["r"])
            
            canvas_state = self.encode_object(self.canvas)
            print("pre send")
            client_endpoint.send(canvas_state)
            print("post send")

            print(f"Sent canvas to {address}")

            # self.clock.tick(env.UPDATE_FREQUENCY)
            listening_thread.join()

        # TODO
        # Send a one time view of the canvas (pygame.PixelArray)
        # Recieve messages from client
        # Bunch them togheter in a list
        # Send list to every connected client

        # while self.is_running:
        #     time.sleep(2)
        #     print(time.time())
        #     ping_msg = self.to_bytes(f"Status check from {env.IP}:{env.PORT}")
        #     client_endpoint.send(ping_msg)
        #     print(f"Pinged {address}")

    def recieve_messages(self, client_endpoint: Socket, address: tuple):
        full_message = client_endpoint.recv(env.BUFFER_SIZE)
        is_object = int(chr(full_message[0]))

        message_length = int(full_message[:env.HEADER_LENGTH])

        while len(full_message) - env.HEADER_LENGTH < message_length:
            full_message += client_endpoint.recv(env.BUFFER_SIZE)
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
        self.point_stack.append(pickle.loads(message))

    def to_bytes(self, message: str):
        # Prefix of zero if message is string
        with_header = f"0{(len(message)+1):<{env.HEADER_LENGTH}}" + message
        return bytes(with_header, "utf-8")

    def encode_object(self, canvas: Optional[pygame.Surface] = None, ):
        ndarray = pygame.surfarray.array3d(canvas)
        pickled = pickle.dumps(ndarray)
        with_header = bytes(f"{len(pickled):<{env.HEADER_LENGTH}}", "utf-8") + pickled
        # return bytes(with_header, "utf-8")
        return with_header

    def shutdown(self):
        self.endpoint.close()
        for thread in self.client_threads:
            thread.join()
        sys.exit()

    
if __name__ == "__main__":
    server = Server()

    try:
        while server.is_running:
            server.accept_clients()
    except KeyboardInterrupt:
        server.shutdown()
    except Exception as e:
        print(e)
    finally:
        server.shutdown()