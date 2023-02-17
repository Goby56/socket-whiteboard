from client import Client
from server import Server

def create_app(endpoint: Client | Server):
    print(type(endpoint))
    if type(endpoint) == Client:
        return AppClient(endpoint)
    else:
        return AppServer(endpoint)


class AppServer:
    def __init__(self, endpoint: Server) -> None:
        pass

class AppClient:
    def __init__(self, endpoint: Client) -> None:
        # self.root = tk.Tk()
        # self.root.geometry(f"{env.DIM[0]}x{env.DIM[1]}")
        # self.root.resizable(False, False)

        # self.canvas = tk.Canvas(self.root, bg="#273136", width=env.DIM[0], height=env.DIM[1])
        # self.canvas.pack()
        # self.brush_down = False
        # self.root.bind("<ButtonPress-1>", lambda event: self.use_brush(True, event))
        # self.root.bind("<ButtonRelease-1>", lambda event: self.use_brush(False, event))
        # self.root.bind("<Motion>", self.send)
        pass




    