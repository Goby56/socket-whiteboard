import socket as sock
from socket import socket as Socket
import pickle

from server import HEADER_LENGTH, IP, PORT
BUFFER_SIZE = 16
class Client:
    def __init__(self, ip: str, port: int, buffer_size: int, header_length: int) -> None:
        self.IP = ip, self.PORT = port, self.BUFFER_SIZE = buffer_size, self.HEADER_LENGTH = header_length
        self.endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.connect((IP, PORT))

    def recieve_messages(self):
        full_message = self.endpoint.recv(self.BUFFER_SIZE)
        message_length = int(msg[:HEADER_LENGTH])

        while len(full_message) - HEADER_LENGTH < message_length:
            full_message += self.endpoint.recv(self.BUFFER_SIZE)
        
        
        

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