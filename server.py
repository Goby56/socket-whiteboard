import socket as sock
from socket import socket as Socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = "2556"
# server_endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
# # Set the socket option level to reuse the adress
# server_endpoint.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1) # args: socket option level, socket option, bool

# server_endpoint.bind((IP, PORT))
# server_endpoint.listen()

# endpoints = [server_endpoint]
# clients = {}

class Server:
    def __init__(self, ip: str, port: int, header_length: int) -> None:
        self.endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.listen()
        self.clients = {}
        self.is_running = True

    def register_clients(self):
        while self.is_running:
            client_endpoint, adress = self.endpoint.accept()
            self.clients[adress] = client_endpoint

    def main():
        # TODO: implement threading/async code execution
        # Threading: https://www.youtube.com/watch?v=IEEhzQoKtQU&t=1s 
        # Asyncio: https://www.youtube.com/watch?v=t5Bo1Je9EmE

    
if __name__ == "__main__":
    server = Server(IP, PORT, HEADER_LENGTH)

    while server.is_running:
        server.main()