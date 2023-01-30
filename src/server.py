import socket as sock
import threading, sys, pygame, time, json, pickle
import env, utils
import numpy as np

if env.IP == "": env.IP = sock.gethostname()

class Server:
    def __init__(self) -> None:
        self.endpoint = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.endpoint.bind((env.IP, env.PORT))
        self.endpoint.listen(env.MAX_SOCKETS)
        print(f"Started server on {env.IP}:{env.PORT}")

        self.whiteboard = np.full(shape=(*env.DIMENSIONS, 3), fill_value=20, dtype=np.uint8)
        self.clients = {}

    def accept_clients(self):
        client_endpoint, address = self.endpoint.accept()
        print(f"Connection from {address} has been made.")

        client_thread = threading.Thread(target=self.handle_client, args=(client_endpoint, address))
        client_thread.start()

        self.clients[address] = {
            "endpoint": client_endpoint,
            "thread": client_thread,
            "point_buffer": []
        }

    def handle_client(self, client_endpoint, address):
        # client_endpoint.send(utils.encode_ndarray(self.whiteboard))
        while True:
            point = self.receive_message(client_endpoint, address)
            for a in self.clients.keys():
                self.clients[a][2].extend(point)

            point_buffer = self.clients[address][2]
            client_endpoint.send(utils.encode_message(point_buffer))
            self.clients[address][2].clear()

    def receive_message(self, client_endpoint: sock.socket, address: tuple):
        header = client_endpoint.recv(env.HEADER_LENGTH) # Grab header
        msg_len = int(header)
        # is_message = True if chr(header[0]) == 0 else False
        reads_required = msg_len // env.BUFFER_SIZE

        _bytes = b""
        for _ in range(reads_required):
            _bytes += client_endpoint.recv(env.BUFFER_SIZE)
        _bytes += client_endpoint.recv(msg_len % env.BUFFER_SIZE)

        # if is_message:
        #     print(_bytes.decode("utf-8"))
        #     return
        # return _bytes
        return list(_bytes)

    # def send_messages(self, client_endpoint: sock.socket, address: tuple):
    #     self.whiteboard = utils.add_points(self.whiteboard, self.point_stack)
    #     for point in self.point_stack:
    #         client_endpoint.send(utils.encode_ndarray(point))
    #     self.point_stack.clear()

    def terminate(self):
        self.endpoint.shutdown(sock.SHUT_RDWR)
        self.endpoint.close()
        for client in self.cleints.values():
            client["thread"].join()
            client["endpoint"].shutdown(sock.SHUT_RDWR)
            client["endpoint"].close()

if __name__ == "__main__":
    server = Server()

    try:
        while True:
            server.accept_clients()
    except Exception as e:
        print(e)
    finally:
        server.shutdown()