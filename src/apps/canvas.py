import json, random, timeit, os, threading
import tkinter as tk
import socket as sock
from PIL import Image, ImageDraw, ImageTk

import env
from app import AppServer, AppClient
from client import Client
from server import Server

DIR = os.path.dirname(__file__)

class CanvasServer(AppServer):
    def __init__(self, server: Server) -> None:
        super().__init__(server)

        with open(os.path.join(DIR, "canvas.json"), "r") as f:
            config = json.load(f)
            setup = config["setup"]
        
        self.canvas_img: Image.Image = Image.new("RGB", (setup["dim"][0], setup["dim"][1]), setup["bg_col"])
        self.draw = ImageDraw.Draw(self.canvas_img)
        self.client_data = {}

    def on_msg_recv(self, data: dict):
        prev_point = self.client_data[data["sender"]]["point"]
        curr_point = data["point"]
        x, y = curr_point["pos"]
        size = curr_point["size"]
        if prev_point["brush_down"] and curr_point["brush_down"]:
            pre_x, pre_y = prev_point["pos"]
            self.draw.line([(pre_x, pre_y), (x, y)], fill=curr_point["color"], width=size)
        elif not prev_point["brush_down"] and curr_point["brush_down"]:
            shape = x-size, y-size, x+size, y+size
            self.draw.ellipse(shape, fill=curr_point["color"], outline=curr_point["color"])
        self.client_data[data["sender"]]["point"] = data["point"]

    def on_handshake(self, client_endpoint: sock.socket, address: str):
        self.client_data[address] = {
            "point": {
                "pos": [0, 0],
                "brush_down": False,
                "size": 0,
                "color": "#000000"
            }
        }

    def start(self):        
        pre_t = timeit.default_timer()
        while self.server.running:
            delta = timeit.default_timer() - pre_t
            if delta * env.TICK_RATE > 1:
                pre_t = timeit.default_timer()
                self._tick()
                
    def _tick(self):
        if len(self.server.clients) < 1:
            return
        data = {
            "canvas": list(self.canvas_img.tobytes())
        }
        self.server.broadcast(data)
    
    def _save_canvas(self):
        pass

    def _load_canvas(self):
        pass

class CanvasClient(AppClient):
    def __init__(self, client: Client) -> None:
        super().__init__(client)

        with open(os.path.join(DIR, "canvas.json"), "r") as f:
            config = json.load(f)
            setup = config["setup"]

        self.DIM = tuple(setup["dim"])

        self.root = tk.Tk()
        self.root.geometry("x".join(map(str, self.DIM)))
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, bg=setup["bg_col"], width=self.DIM[0], height=self.DIM[1])
        self.canvas.pack()
        self.brush_down = False
        self.root.bind("<ButtonPress-1>", lambda event: self._use_brush(True, event))
        self.root.bind("<ButtonRelease-1>", lambda event: self._use_brush(False, event))
        self.root.bind("<Motion>", self._send)

        self.color = "#%02x%02x%02x" % tuple(random.randint(0, 255) for _ in range(3))

    def _use_brush(self, value: bool, event: tk.Event):
        self.brush_down = value
        if value: self._send(event)

    def _send(self, event: tk.Event):
        data = {
            "point": {
                "pos": [event.x, event.y],
                "brush_down": self.brush_down,
                "size": 10,
                "color": self.color
            }
        }
        self.client.transmit(data)

    def start(self):
        self.root.mainloop()

    def on_msg_recv(self, data: dict):
        canvas_bytes = bytes(data["canvas"])
        canvas_image = Image.frombytes("RGB", self.DIM, canvas_bytes)
        canvas_photo = ImageTk.PhotoImage(canvas_image)
        self.canvas.create_image(0, 0, image=canvas_photo)
    