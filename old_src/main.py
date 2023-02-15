import tkinter as tk
import env, utils, client
import random

class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry(f"{env.DIM[0]}x{env.DIM[1]}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, bg="#273136", width=env.DIM[0], height=env.DIM[1])
        self.canvas.pack()
        self.brush_down = False
        self.root.bind("<ButtonPress-1>", lambda event: self.use_brush(True, event))
        self.root.bind("<ButtonRelease-1>", lambda event: self.use_brush(False, event))
        self.root.bind("<Motion>", self.send)

        self.client = client.Client(self.draw)
        self.prev_point = {}
        self.rgb = [random.randint(0, 255) for _ in range(3)]

    def use_brush(self, value: bool, event: tk.Event):
        self.brush_down = value
        if value: self.send(event)

    def send(self, event: tk.Event):
        x, y, size = event.x, event.y, 10
        self.client.endpoint.send(utils.encode_values(x, y, size, *self.rgb, int(self.brush_down)))
    
    def draw(self, x, y, size, red, green, blue, use, port):
        color = "#%02x%02x%02x" % (red, green, blue) 
        exists = port in self.prev_point.keys()
        if exists and not use:
            del self.prev_point[port]
        elif exists and use:
            pre_x, pre_y = self.prev_point[port]
            self.canvas.create_line(pre_x, pre_y, x, y, width=size, fill=color, capstyle=tk.ROUND)
        elif not exists and use:
            self.canvas.create_oval(x-size/2, y-size/2, x+size/2, y+size/2, fill=color, outline=color)
        if use:
            self.prev_point[port] = x, y
        

if __name__ == "__main__":
    app = App()
    app.root.mainloop()
    app.client.shutdown()