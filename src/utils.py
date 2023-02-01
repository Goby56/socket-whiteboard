import env

def encode_values(*values: int):
    data = bytes(",".join(map(str, values)), "utf-8")
    header = bytes(f"{len(data):<{env.HEADER_LENGTH}}", "utf-8")
    return header + data

def decode_message(data: bytes):
    values = list(map(int, data.decode("utf-8").split(",")))
    return values

# class PointBuffer:
#     client_points = {}
#     def __init__(self, x, y, size, red, green, blue, port) -> None:
#         self.x = x
#         self.y = y
#         self.w = size
        
#         self.c = 