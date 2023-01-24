import socket as s
import pickle

from server import HEADER_LENGTH

endpoint: s.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
endpoint.connect((s.gethostname(), 6969))

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