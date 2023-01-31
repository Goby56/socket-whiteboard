import threading
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
        self.root.bind("<ButtonPress-1>", lambda event: self.use_brush(True))
        self.root.bind("<ButtonRelease-1>", lambda event: self.use_brush(False))
        self.root.bind("<Motion>", self.send)

        self.client = client.Client(self.draw)
        self.receiving_thread = threading.Thread(target=self.client.receive_messages)
        self.receiving_thread.start()

    def use_brush(self, value: bool):
        self.brush_down = value

    def send(self, event):
        if not self.brush_down:
            return
        x, y, r = event.x, event.y, 10
        print(x, y, r)
        self.client.endpoint.send(utils.encode_values(x, y, r, 200, 200, 200))
    
    def draw(self, x, y, r, red, green, blue):
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#e5f2e4", outline="#e5f2e4")


if __name__ == "__main__":
    app = App()
    app.root.mainloop()