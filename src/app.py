import socket as sock

class AppServer:
    def __init__(self, server) -> None:
        self.server = server

    def start(self):
        raise NotImplementedError()

    def on_msg_recv(self, data: dict):
        raise NotImplementedError()

    def on_handshake(self, client_endpoint: sock.socket, address: str):
        raise NotImplementedError()

class AppClient:
    def __init__(self, client) -> None:
        self.client = client

    def start(self):
        raise NotImplementedError()
    
    def on_msg_recv(self, data: dict):
        raise NotImplementedError()
