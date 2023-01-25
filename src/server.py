import socket as sock
from socket import socket as Socket
import threading, sys, time, json, os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

class Server:
    def __init__(self) -> None:
        with open(CONFIG_PATH, "r") as f:
            self.config = json.load(f)
            self.IP, self.PORT = self.config["server"]["ip"], self.config["server"]["port"]
            self.MAX_SOCKETS, self.HEADER_LENGTH = self.config["server"]["max_sockets"], self.config["server"]["header_length"]
            if self.IP == "":
                self.IP = sock.gethostname()
        self.endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
        # # Set the socket option level to reuse the adress
        self.endpoint.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.endpoint.bind((self.IP, self.PORT))
        self.endpoint.listen(self.MAX_SOCKETS)

        print(f"Started server on {self.IP}:{self.PORT}")

        self.clients = {}
        self.client_threads = []
        self.is_running = True
        
    def accept_clients(self):
        client_endpoint, address = self.endpoint.accept()
        print(f"Connection from {address} has been made.")

        new_thread = threading.Thread(target=self.handle_client, args=(client_endpoint, address))
        new_thread.start()
        self.client_threads.append(new_thread)

        # client_threads = [threading.Thread(target=self.accept_clients) for _ in range(self.MAX_SOCKETS)]
        # TODO: implement threading/async code execution
        # Threading: https://www.youtube.com/watch?v=IEEhzQoKtQU&t=1s 
        # Asyncio: https://www.youtube.com/watch?v=t5Bo1Je9EmE

    def handle_client(self, client_endpoint: Socket, address: tuple):
        welcome_msg = self.to_bytes(f"Joined server {self.IP}:{self.PORT}")
        client_endpoint.send(welcome_msg)
        
        # TODO
        # Send a one time view of the canvas (pygame.PixelArray)
        # Recieve messages from client
        # Bunch them togheter in a list
        # Send list to every connected client

        
        # client_endpoint.recv()

        while self.is_running:
            time.sleep(2)
            ping_msg = self.to_bytes(f"Status check from {self.IP}:{self.PORT}")
            client_endpoint.send(ping_msg)
            print(f"Pinged {address}")


    def to_bytes(self, message: str):
        # Prefix of zero if message is string
        with_header = f"0{(len(message)+1):<{self.HEADER_LENGTH}}" + message
        return bytes(with_header, "utf-8")

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