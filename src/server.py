import socket as sock
import threading, timeit, argparse
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
        
        self.state = {}
        self.clients = {}
        self.accepting_thread = threading.Thread(target=self.accept_clients)
        self.tick_loop()

    def accept_clients(self):
        while self.running:
            client_endpoint, address = self.endpoint.accept()
            print("Connection from", address[1])

            client_endpoint.send(utils.encode_data(self.persistent_data))
            listening_thread = threading.Thread(target=self.listen, args=(client_endpoint, address))
            listening_thread.start()

            self.clients[address] = {
                "endpoint": client_endpoint,
                "thread": listening_thread,
                "data": {}
            }

    def tick_loop(self):
        pre_t = timeit.default_timer()
        while self.running:
            delta = timeit.default_timer() - pre_t
            if delta * env.TICK_RATE > 1:
                pre_t = timeit.default_timer()
                for addr, client in self.clients:
                    self.tick(client["endpoint"], addr)

    def tick(self, client_endpoint: sock.socket, address: tuple):
        client_endpoint.send(utils.encode_data({"value": 1}, address))

    def listen(self, client_endpoint: sock.socket, address: tuple):
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
                _bytes += self.endpoint.recv(env.BUFFER_SIZE)
            _bytes += self.endpoint.recv(msg_len % env.BUFFER_SIZE)

            self.clients[address]["data"].append(utils.decode_message(_bytes))

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
    mod = __import__(f"apps.{args.application}", fromlist=["create_app"])
    app = getattr(mod, "create_app")(Server())