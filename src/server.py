import socket as sock
import threading
import env, utils

if env.IP == "": env.IP = sock.gethostname()

class Server:
    def __init__(self) -> None:
        self.endpoint = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.endpoint.bind((env.IP, env.PORT))
        self.endpoint.listen(env.MAX_SOCKETS)
        print(f"Started server on {env.IP}:{env.PORT}")

        self.clients = {}
        self.point_buffer = []

    def accept_clients(self):
        client_endpoint, address = self.endpoint.accept()
        print(f"Connection from {address} has been made.")

        client_thread = threading.Thread(target=self.handle_client, args=(client_endpoint,))
        client_thread.start()
        
        self.clients[address] = {
            "endpoint": client_endpoint,
            "thread": client_thread
        }

    def handle_client(self, client_endpoint: sock.socket):
        for i in range(0, len(self.point_buffer), 6):
            client_endpoint.send(utils.encode_values(*self.point_buffer[i:i+6]))
        while True:
            point = self.receive_message(client_endpoint)
            self.point_buffer.extend(point)
            for client in self.clients.values():
                client["endpoint"].send(utils.encode_values(*point))

    def receive_message(self, client_endpoint: sock.socket):
        header = client_endpoint.recv(env.HEADER_LENGTH)
        msg_len = int(header)
        reads_required = msg_len // env.BUFFER_SIZE

        _bytes = b""
        for _ in range(reads_required):
            _bytes += client_endpoint.recv(env.BUFFER_SIZE)
        _bytes += client_endpoint.recv(msg_len % env.BUFFER_SIZE)

        return utils.decode_message(_bytes)

    def terminate(self):
        self.endpoint.shutdown(sock.SHUT_RDWR)
        self.endpoint.close()
        for client in self.cleints.values():
            client["endpoint"].shutdown(sock.SHUT_RDWR)
            client["endpoint"].close()
            client["thread"].join()

if __name__ == "__main__":
    server = Server()

    try:
        while True:
            server.accept_clients()
    except Exception as e:
        print(e)
    finally:
        server.shutdown()