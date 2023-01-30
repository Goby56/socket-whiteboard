import pygame, sys, json, threading, os
from client import Client
import numpy as np
import env, utils

class App:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(env.DIMENSIONS)
        self.window.fill((20, 20, 20))
        pygame.display.set_caption("Socket whiteboard")

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.client = Client()

    def main(self):
        receiving_thread = threading.Thread(target=self.client.receive_message)
        receiving_thread.start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.client_listener.join()
                pygame.quit()
                sys.exit()

        self.clock.tick(env.FPS)
        receiving_thread.join()

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            r, g, b = 200, 200, 200
            radius = 10
            point = [x, y, r, g, b, radius]
            self.client.endpoint.send(utils.encode_list(point))

        self.render()
        pygame.display.update()

    def render(self):
        self.client.whiteboard = utils.add_points(self.client.whiteboard, self.client.point_buffer)
        self.client.point_buffer.clear()
        
        self.window.blit(utils.surface_from(self.client.whiteboard), (0,0))
        

if __name__ == "__main__":
    app = App()

    while app.is_running:
        app.main()