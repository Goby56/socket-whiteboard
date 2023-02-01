import tkinter as tk
import env, utils, client

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
        # self.prev_point = {}

    def use_brush(self, value: bool, event: tk.Event):
        self.brush_down = value
        if value: self.send(event)

    def send(self, event: tk.Event):
        if not self.brush_down:
            return
        x, y, w, r, g, b = event.x, event.y, 10, 200, 200, 200
        self.client.endpoint.send(utils.encode_values(x, y, w, r, g, b))
    
    def draw(self, x, y, r, red, green, blue):
        # curr_point = (x, y, width, red, green, blue, port)
        # if port not in self.prev_point.keys():
        #     self.canvas.create_oval(x-width/2, y-width/2, x+width/2, y+width/2, fill="#e5f2e4", outline="#e5f2e4")
        #     self.prev_point[port] = x, y
        #     return
        
        # pre_x, pre_y = self.prev_point[port]
        # self.canvas.create_line(pre_x, pre_y, x, y, width=width, fill="#e5f2e4")
        # self.prev_point[port] = x, y
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#e5f2e4", outline="#e5f2e4")

# class Point:
#     clients = {}
#     def __init__(self) -> None:
#         pass
    
#     @classmethod
#     def exists(cls, port):
#         return True if port in cls.clients.keys() else False

#     def add(cls, port)
        


if __name__ == "__main__":
    app = App()
    app.root.mainloop()