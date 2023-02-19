import threading, timeit, argparse, importlib, time
import socket as sock

import env, utils
from app import AppServer

if env.IP == "": env.IP = sock.gethostname()

class Server:
    def __init__(self, Application) -> None:
        self.endpoint = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.endpoint.bind((env.IP, env.PORT))
        self.endpoint.listen(env.MAX_SOCKETS)
        
        print(f"Server running at {env.IP}:{env.PORT}")
        self.running = True
        
        self.app: AppServer = Application(self)
        self.clients = {}
        self.accepting_thread = threading.Thread(target=self.accept_clients)
        self.accepting_thread.start()
        self.app.start()

    def accept_clients(self):
        while self.running:
            client_endpoint, address = self.endpoint.accept()
            address = address[0] + ":" + str(address[1])
            print("Connection from", address)

            listening_thread = threading.Thread(target=self.listen, args=(client_endpoint, address))
            listening_thread.start()

            self.clients[address] = {
                "endpoint": client_endpoint,
                "thread": listening_thread
            }

    def broadcast(self, data: dict):
        for client in self.clients.values():
            self.send_to(client["endpoint"], data)

    def send_to(self, client_endpoint: sock.socket, data: dict):
        message = utils.encode_data(data)
        client_endpoint.send(message)

    def listen(self, client_endpoint: sock.socket, address: str):
        self.app.on_handshake(client_endpoint, address)
        while self.running:
            try:
                header = client_endpoint.recv(env.HEADER_LENGTH)
                if not header: raise ConnectionResetError
            except ConnectionResetError:
                client_endpoint.shutdown(sock.SHUT_RDWR)
                print(address, "disconnected")
                return
            
            msg_len = int(header)
            reads_required = msg_len // env.BUFFER_SIZE

            _bytes = b""
            for _ in range(reads_required):
                _bytes += client_endpoint.recv(env.BUFFER_SIZE)
            _bytes += client_endpoint.recv(msg_len % env.BUFFER_SIZE)

            data = utils.decode_message(_bytes)
            data["sender"] = address
            self.app.on_msg_recv(data)

    def shutdown(self):
        self.endpoint.shutdown(sock.SHUT_RDWR)
        self.endpoint.close()
        for client in self.clients:
            client["endpoint"].shutdown(sock.SHUT_RDWR)
            client["endpoint"].close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Serve a given application by passing it as an argument")
    valid_apps = utils.applications_implemented()
    parser.add_argument("application", help=f"Valid applications: {valid_apps}")
    args = parser.parse_args()
    module = importlib.import_module(f"apps.{args.application}")
    App = module.__dict__[f"{args.application.capitalize()}Server"]
    client = Server(App)
    