import pygame, sys, json, threading, os, random
from client import Client
import tkinter as tk
import numpy as np
import env, utils

# class App:
#     def __init__(self) -> None:
#         self.window = pygame.display.set_mode(env.DIMENSIONS)
#         self.window.fill((20, 20, 20))
#         pygame.display.set_caption("Socket whiteboard")
#         self.clock = pygame.time.Clock()

#         self.client = Client()
#         self.receiving_thread = threading.Thread(target=self.client.receive_message)
#         self.receiving_thread.start()

#     def main(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.client.terminate()
#                 self.receiving_thread.join()
#                 pygame.quit()
#                 sys.exit()

#         if pygame.mouse.get_pressed()[0]:
#             x, y = pygame.mouse.get_pos()
#             r, g, b = [random.randint(0, 255) for x in range(3)]
#             radius = 4
#             point = [x, y, r, g, b, radius]
#             self.client.endpoint.send(utils.encode_values(*point))

#         self.render()
#         # self.clock.tick(env.FPS)
#         pygame.display.update()

#     def render(self):
#         surface = pygame.pixelcopy.make_surface(self.client.whiteboard)
#         for i in range(0, len(self.client.point_buffer), 6):
#             if len(self.client.point_buffer) % 6 != 0: break
#             x, y, r, g, b, radius = self.client.point_buffer[i:i+6]
#             del self.client.point_buffer[i:i+6]
#             pygame.draw.circle(surface, (r, g, b), (x, y), radius)
#         pygame.pixelcopy.surface_to_array(self.client.whiteboard, surface)
#         self.window.blit(surface, (0,0))

class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry(f"{env.DIM[0]}x{env.DIM[1]}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, bg="blue", width=env.DIM[0], height=env.DIM[1])
        self.canvas.pack()
        self.brush_down = False
        self.root.bind("<ButtonPress-1>", lambda event: self.use_brush(True))
        self.root.bind("<ButtonRelease-1>", lambda event: self.use_brush(False))
        self.root.bind("<Motion>", self.send)

        self.client = Client(self.draw)
        self.receiving_thread = threading.Thread(target=self.client.receive_message)
        self.receiving_thread.start()

    def use_brush(self, value: bool):
        self.brush_down = value

    def send(self, event):
        if not self.brush_down:
            return
        x, y, r = event.x, event.y, 100
        print(x, y, r)
        self.client.endpoint.send(utils.encode_values(x, y, r, 200, 200, 200))
    
    def draw(self, x, y, r, red, green, blue):
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#e5f2e4")



if __name__ == "__main__":
    app = App()
    app.root.mainloop()