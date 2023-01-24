import socket as sock
from socket import socket as Socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = "2556"
server_endpoint = Socket(sock.AF_INET, sock.SOCK_STREAM)
# Set the socket option level to reuse the adress
server_endpoint.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1) # args: socket option level, socket option, bool

server_endpoint.bind((IP, PORT))
server_endpoint.listen()

endpoints = [server_endpoint]
clients = {}

def receive_message(client_socket: Socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}    
    except:
        False

while True:
    read_endpoints, _, exception_endpoints = select.select(endpoints, [], endpoints)
