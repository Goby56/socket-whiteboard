import threading, argparse, importlib
import socket as sock

import env, utils
from app import AppClient

if env.IP == "": env.IP = sock.gethostname()

class Client:
    def __init__(self, Application) -> None:
        self.endpoint = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.connect((env.IP, env.PORT))
        print(f"Connected to {env.IP}:{env.PORT}")
        
        self.app: AppClient = Application(self)

        self.receiving_thread = threading.Thread(target=self._listen)
        self.receiving_thread.start()

        self.app.start()

    def transmit(self, data: dict):
        message = utils.encode_data(data)
        self.endpoint.send(message)

    def _listen(self):
        while True:
            header = self.endpoint.recv(env.HEADER_LENGTH)
            msg_len = int(header)
            reads_required = msg_len // env.BUFFER_SIZE

            _bytes = b""
            for _ in range(reads_required):
                _bytes += self.endpoint.recv(env.BUFFER_SIZE)
            _bytes += self.endpoint.recv(msg_len % env.BUFFER_SIZE)

            data = utils.decode_message(_bytes)
            self.app.on_msg_recv(data)
    
    def _shutdown(self):
        self.endpoint.shutdown(sock.SHUT_RDWR)
        self.endpoint.close()
        self.receiving_thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Connect to a given application by passing it as an argument")
    parser.add_argument("application", help="Valid applications:")
    args = parser.parse_args()
    module = importlib.import_module(f"apps.{args.application}")
    App = module.__dict__[f"{args.application.capitalize()}Client"]
    client = Client(App)