import env

def encode_values(*values: int):
    data = bytes(",".join(map(str, values)), "utf-8")
    header = bytes(f"{len(data):<{env.HEADER_LENGTH}}", "utf-8")
    return header + data

def decode_message(data: bytes):
    values = list(map(int, data.decode("utf-8").split(",")))
    return values