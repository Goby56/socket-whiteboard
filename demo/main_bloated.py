import pygame, sys, json, threading, os
from client import Client
import numpy as np
import env

# CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

class App:
    def __init__(self) -> None:
        # with open(CONFIG_PATH, "r") as f:
        #     self.config = json.load(f)
            
        self.window = pygame.display.set_mode(env.DIM)
        self.window.fill((20, 20, 20))
        pygame.display.set_caption("Socket whiteboard")

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.client = Client()
        self.client_listener = threading.Thread(target=self.client.listen)
        self.client_listener.start()

    def main(self):
        self.event_handler()

        self.render()

        # TODO
        # Draw lines from the client's point stack

        pygame.display.update()
        self.clock.tick(env.FPS)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.client_listener.join()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                point = {
                    "r": 10,
                    "c": (230,230,230),
                    "p": pygame.mouse.get_pos()
                }
                self.client.send(point)

    def render(self):
        # if not self.client.has_canvas:
        #     self.window.fill((20, 20, 20))
        #     # TODO: Add buffering symbol
        #     return
        self.window.blit(self.client.canvas, (0,0))
        

if __name__ == "__main__":
    app = App()

    while app.is_running:
        app.main()