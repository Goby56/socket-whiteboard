import socket as sock
from socket import socket as Socket
import threading, sys, time

HEADER_LENGTH = 10
MAX_SOCKETS = 12
IP = sock.gethostname()
PORT = 2556
# server_endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
# # Set the socket option level to reuse the adress
# server_endpoint.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1) # args: socket option level, socket option, bool

# server_endpoint.bind((IP, PORT))
# server_endpoint.listen()

# endpoints = [server_endpoint]
# clients = {}

class Server:
    def __init__(self, ip: str, port: int, max_sockets: int, header_length: int) -> None:
        self.IP, self.PORT, self.MAX_SOCKETS, self.HEADER_LENGTH = ip, port, max_sockets, header_length
        self.endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.bind((self.IP, self.PORT))
        self.endpoint.listen(self.MAX_SOCKETS)

        # with concurrent.futures.ThreadPoolExecutor as executor:
        #     self.client_futures = [executor.submit(self.endpoint.accept()) for _ in range(self.MAX_SOCKETS)]

        self.clients = {}
        self.client_threads = []
        self.is_running = True
        
    def main(self):
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

        while self.is_running:
            time.sleep(2)
            ping_msg = self.to_bytes(f"Status check from {self.IP}:{self.PORT}")
            client_endpoint.send(ping_msg)
            print(f"Pinged {address}")


    def to_bytes(self, message: str):
        with_header = f"{len(message):<{self.HEADER_LENGTH}}" + message
        return bytes(with_header, "utf-8")

    def shutdown(self):
        self.endpoint.close()
        for thread in self.client_threads:
            thread.join()

    
if __name__ == "__main__":
    server = Server(IP, PORT, MAX_SOCKETS, HEADER_LENGTH)

    try:
        while server.is_running:
            server.main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(e)
    finally:
        server.shutdown()