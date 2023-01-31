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

def encode_list(ints: list[int]):
    print(ints)
    data = bytes(ints)
    header = bytes(f"{len(data):<{env.HEADER_LENGTH}}", "utf-8")
    return data + header

def encode_point(x, y, radius, red, green, blue):
    data = bytes(f"{x},{y},{radius},{red},{green},{blue}", "utf-8")
    header = bytes(f"{len(data):<{env.HEADER_LENGTH}}", "utf-8")
    return header + data

def decode_point(data: bytes):
    # x, y, radius, red, green, blue = map(int, data.split(","))
    return list(map(int, data.decode("utf-8").split(",")))

def encode_values(*values: int):
    data = bytes(",".join(map(str, values)), "utf-8")
    header = bytes(f"{len(data):<{env.HEADER_LENGTH}}", "utf-8")
    return header + data

def decode_message(data: bytes):
    values = list(map(int, data.decode("utf-8").split(",")))
    return values

def surface_from(whiteboard: np.ndarray) -> pygame.Surface:
    return pygame.pixelcopy.make_surface(whiteboard)

def add_points(whiteboard: np.ndarray, point_buffer: list) -> np.ndarray :
    surface = surface_from(whiteboard)
    for i in range(len(point_buffer)):
        print(point_buffer[i:i+6])
        x, y, radius, red, green, blue = point_buffer[i:i+6]
        pygame.draw.circle(surface, (red, green, blue), (x, y), radius)
    pygame.pixelcopy.surface_to_array(whiteboard, surface)
    return whiteboard

# print(decode_point(f"200,200,3,10,10,10"))
# print(encode_point(200, 200, 3, 10, 10, 10))