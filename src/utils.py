import env
import pygame, pickle
import numpy as np
from typing import Optional

def encode_str(string: str) -> bytes:
    message = f"0{(len(string)+1):<{env.HEADER_LENGTH}}" + string
    return bytes(message, "utf-8")

def encode_ndarray(array: np.ndarray) -> bytes:
    pickled = pickle.dumps(array)
    header = bytes(f"{len(pickled):<{env.HEADER_LENGTH}}", "utf-8")
    return header + pickled

def encode_message(ints: list[int]):
    data = bytes(ints)
    header = bytes(f"{len(data):<{env.HEADER_LENGTH}}", "utf-8")
    return data + header

def surface_from(whiteboard: np.ndarray) -> pygame.Surface:
    return pygame.pixelcopy.make_surface(whiteboard)

def add_points(whiteboard: np.ndarray, points: list) -> np.ndarray :
    surface = surface_from(whiteboard)
    for i in range(len(points)):
        x, y, radius, red, green, blue = points[i:i+6]
        pygame.draw.circle(surface, (red, green, blue), (x, y), radius)
    pygame.pixelcopy.surface_to_array(whiteboard, surface)
    return whiteboard