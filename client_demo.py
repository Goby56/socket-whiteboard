import socket as s
import pickle

HEADER_SIZE = 10

endpoint: s.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
endpoint.connect((s.gethostname(), 2556))

# while True:
#     full_msg = b""
#     new_msg = True
#     while True:
#         msg = endpoint.recv(16)
#         if new_msg:
#             msg_len = int(msg[:HEADER_SIZE])
#             print(f"new message length: {msg_len}")
#             new_msg = False
        
#         full_msg += msg
#         print("appended to message")

#         if len(full_msg)-HEADER_SIZE == msg_len:
#             print("full msg recieved")
#             print(full_msg)
#             dct = pickle.loads(full_msg[HEADER_SIZE:])
#             print(dct)
#             new_msg = True
#             full_msg = b""




while True:
    full_msg = ""
    new_msg = True
    while True:
        msg = endpoint.recv(16)
        if new_msg:
            msg_len = int(msg[:HEADER_SIZE])
            new_msg = False
        
        full_msg += msg.decode("utf-8")

        if len(full_msg)-HEADER_SIZE == msg_len:
            print(full_msg[HEADER_SIZE:])
            new_msg = True
            full_msg = ""