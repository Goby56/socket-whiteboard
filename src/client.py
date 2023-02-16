import socket as sock
import threading, argparse
import env, utils

if env.IP == "": env.IP = sock.gethostname()

class Client:
    def __init__(self) -> None:
        self.endpoint = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.connect((env.IP, env.PORT))
        print(f"Connected to {env.IP}:{env.PORT}")

        self.data = {}
        self.server_state = {}

        self.receiving_thread = threading.Thread(target=self.receive_messages)
        self.receiving_thread.start()

    def tick(self):
        self.endpoint.send(utils.encode_data(self.data))

    def receive_messages(self):
        while True:
            header = self.endpoint.recv(env.HEADER_LENGTH)
            msg_len = int(header)
            reads_required = msg_len // env.BUFFER_SIZE

            _bytes = b""
            for _ in range(reads_required):
                _bytes += self.endpoint.recv(env.BUFFER_SIZE)
            _bytes += self.endpoint.recv(msg_len % env.BUFFER_SIZE)

            self.update_state(utils.decode_message(_bytes))

    def update_state(self, new_state: dict):
        self.server_state = new_state
    
    def shutdown(self):
        self.endpoint.shutdown(sock.SHUT_RDWR)
        self.endpoint.close()
        self.receiving_thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Connect to a given application by passing it as an argument")
    parser.add_argument("application", help="Valid applications:")
    args = parser.parse_args()
    mod = __import__(f"apps.{args.application}", fromlist=["App"])
    app = getattr(mod, "App")(Client())