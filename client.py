import socket as sock
from socket import socket as Socket
import pickle

from server import HEADER_LENGTH, IP, PORT

class Client:
    def __init__(self) -> None:
        self.endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.connect((IP, PORT))

while True:
    full_msg = b""
    new_msg = True
    while True:
        msg = endpoint.recv(16)
        if new_msg:
            msg_len = int(msg[:HEADER_LENGTH])
            print(f"new message length: {msg_len}")
            new_msg = False
        
        full_msg += msg
        print("appended to message")

        if len(full_msg)-HEADER_LENGTH == msg_len:
            print("full msg recieved")
            print(full_msg)
            dct = pickle.loads(full_msg[HEADER_LENGTH:])
            print(dct)
            new_msg = True
            full_msg = b""



""" Buffer
while True:
    full_msg = ""
    new_msg = True
    while True:
        msg = endpoint.recv(16)
        if new_msg:
            msg_len = int(msg[:HEADER_SIZE])
            print(f"new message length: {msg_len}")
            new_msg = False
        
        full_msg += msg.decode("utf-8")

        if len(full_msg)-HEADER_SIZE == msg_len:
            print("full msg recieved")
            print(full_msg[HEADER_SIZE:])
            new_msg = True
            full_msg = ""
"""