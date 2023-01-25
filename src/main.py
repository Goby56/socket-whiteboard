import pygame, sys, json, threading, os
from client import Client
import numpy as np

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

class App:
    def __init__(self) -> None:
        with open(CONFIG_PATH, "r") as f:
            self.config = json.load(f)
            
        self.DIMENSIONS = self.config["app"]["dim"]
        self.window = pygame.display.set_mode(self.DIMENSIONS)
        self.window.fill((20, 20, 20))
        pygame.display.set_caption("Socket whiteboard")

        self.FPS = self.config["app"]["fps"]
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.client = Client()

    def main(self):
        self.event_handler()
        client_listener = threading.Thread(target=self.client.listen())
        client_listener.start()

        # TODO
        # Draw lines from the client's point stack

        pygame.display.update()
        app.clock.tick(app.FPS)
        client_listener.join()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def render(self):
        if not self.client.has_canvas:
            self.window.fill((20, 20, 20))
            # TODO: Add buffering symbol
            return
        self.window.blit(self.client.canvas.make_surface(), (0,0))
        

if __name__ == "__main__":
    app = App()

    while app.is_running:
        app.main()