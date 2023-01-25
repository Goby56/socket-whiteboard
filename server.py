import socket as sock
from socket import socket as Socket
import select
import threading, sys

HEADER_LENGTH = 10
MAX_SOCKETS = 12
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
    def __init__(self, ip: str, port: int, max_sockets: int, header_length: int) -> None:
        self.endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.listen()


        self.clients = {}
        self.client_threads = []
        self.is_running = True
        

    def accept_clients(self):
        client_endpoint, adress = self.endpoint.accept()
        self.clients[adress] = client_endpoint

    def main(self):
        
        client_threads = [threading.Thread(target=self.accept_clients) for _ ]
        # TODO: implement threading/async code execution
        # Threading: https://www.youtube.com/watch?v=IEEhzQoKtQU&t=1s 
        # Asyncio: https://www.youtube.com/watch?v=t5Bo1Je9EmE

    
if __name__ == "__main__":
    server = Server(IP, PORT, MAX_SOCKETS, HEADER_LENGTH)

    while server.is_running:
        try:
            server.main()
        except KeyboardInterrupt:
            sys.exit(0)