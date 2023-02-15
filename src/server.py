import socket as sock
import threading, timeit
import env, utils

if env.IP == "": env.IP = sock.gethostname()

class Server:
    def __init__(self) -> None:
        self.endpoint = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.endpoint.bind((env.IP, env.PORT))
        self.endpoint.listen(env.MAX_SOCKETS)

        print(f"Listening on {env.IP}:{env.PORT}")
        self.running = True

        self.clients = []
        self.accepting_thread = threading.Thread(target=self.accept_clients)
        self.tick_loop()

    def accept_clients(self):
        while self.running:
            client_endpoint, address = self.endpoint.accept()
            print("Connection from", address[1])
            self.clients.append(Client(client_endpoint, address))

            client_thread = threading.Thread(target=self.handle_client, args=(client_endpoint, address[1]))
            client_thread.start()

    def tick_loop(self):
        pre_t = timeit.default_timer()
        while self.running:
            delta = timeit.default_timer() - pre_t
            if delta * env.TICK_RATE > 1:
                pre_t = timeit.default_timer()
                for client in self.clients:
                    client.tick()

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

    def shutdown(self):
        self.endpoint.shutdown(sock.SHUT_RDWR)
        self.endpoint.close()
        for client in self.clients:
            client.endpoint.shutdown(sock.SHUT_RDWR)
            client.endpoint.close()


class Client:
    def __init__(self, endpoint: sock.socket, address: sock._RetAddress) -> None:
        self.endpoint = endpoint
        self.ip = address[0], self.port = address[1]

        self.events = []

    def tick(self):
        pass

    def listen(self):
        while True:
            try:
                header = self.endpoint.recv(env.HEADER_LENGTH)
                if not header: raise ConnectionResetError
            except ConnectionResetError:
                self.endpoint.shutdown(sock.SHUT_RDWR)
                print(self.port, "disconnected")
                return
            
            msg_len = int(header)
            reads_required = msg_len // env.BUFFER_SIZE

            _bytes = b""
            for _ in range(reads_required):
                _bytes += self.endpoint.recv(env.BUFFER_SIZE)
            _bytes += self.endpoint.recv(msg_len % env.BUFFER_SIZE)

            self.events.append(utils.decode_message(_bytes))

if __name__ == "__main__":
    server = Server()