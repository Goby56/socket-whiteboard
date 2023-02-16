from ..client import Client
from ..server import Server

class App:
    def __init__(self, endpoint: Client | Server) -> None:
        if type(endpoint) == Client:
            pass