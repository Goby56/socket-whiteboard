import socket as sock
import pickle, pygame, time, threading, sys, json
import env, utils
import numpy as np

if env.IP == "": env.IP = sock.gethostname()

class Client:
    def __init__(self, draw_func: callable) -> None:
        self.endpoint = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.connect((env.IP, env.PORT))
        print(f"Joined server on {env.IP}:{env.PORT}")

        self.draw = draw_func

        # self.whiteboard = np.full(shape=(*env.DIM, 3), fill_value=20, dtype=np.uint8)
        # self.point_buffer = []

    def receive_messages(self):
        while True:
            header = self.endpoint.recv(env.HEADER_LENGTH)
            msg_len = int(header)
            reads_required = msg_len // env.BUFFER_SIZE

            _bytes = b""
            for _ in range(reads_required):
                _bytes += self.endpoint.recv(env.BUFFER_SIZE)
            _bytes += self.endpoint.recv(msg_len % env.BUFFER_SIZE)

            self.draw(*utils.decode_message(_bytes))
            # self.point_buffer.extend(utils.decode_message(_bytes))
    
    def terminate(self):
        self.endpoint.shutdown(sock.SHUT_RDWR)
        self.endpoint.close()