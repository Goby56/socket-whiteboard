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
        print(f"Listening on {env.IP}:{env.PORT}")

        self.clients = {}
        self.point_buffer = []

    def accept_clients(self):
        client_endpoint, address = self.endpoint.accept()
        print("Connection from", address[1])

        client_thread = threading.Thread(target=self.handle_client, args=(client_endpoint, address[1]))
        client_thread.start()
        
        self.clients[address[1]] = {
            "endpoint": client_endpoint,
            "thread": client_thread
        }

    def handle_client(self, client_endpoint: sock.socket, port: int):
        for i in range(0, len(self.point_buffer), 8):
            client_endpoint.send(utils.encode_values(*self.point_buffer[i:i+8]))
        while True:
            point = self.receive_message(client_endpoint, port)
            if point == None: break
            self.point_buffer.extend([*point, 0])
            for p, client in self.clients.items():
                if p == port: # port = 0 to the client being handled
                    client["endpoint"].send(utils.encode_values(*point, 0))
                    continue
                client["endpoint"].send(utils.encode_values(*point, port))

    def receive_message(self, client_endpoint: sock.socket, port: int):
        try:
            header = client_endpoint.recv(env.HEADER_LENGTH)
            if not header: raise ConnectionResetError
        except ConnectionResetError:
            self.disconnect(port)
            del self.clients[port]
            print(port, "disconnected")
            return
        
        msg_len = int(header)
        reads_required = msg_len // env.BUFFER_SIZE

        _bytes = b""
        for _ in range(reads_required):
            _bytes += client_endpoint.recv(env.BUFFER_SIZE)
        _bytes += client_endpoint.recv(msg_len % env.BUFFER_SIZE)

        return utils.decode_message(_bytes)

    def disconnect(self, port: int):
        self.clients[port]["endpoint"].shutdown(sock.SHUT_RDWR)
        self.clients[port]["endpoint"].close()

    def shutdown(self):
        self.endpoint.shutdown(sock.SHUT_RDWR)
        self.endpoint.close()
        for port in self.clients.keys():
            self.disconnect(port)
            self.clients[port]["thread"].join()

if __name__ == "__main__":
    server = Server()

    while True:
        server.accept_clients()