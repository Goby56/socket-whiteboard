import time, json, glob, re
import env

# TODO MAKE OWN BYTES FORMAT FOR ANY TYPE OF DATA

def encode_data(data: dict):
    data["sent"] = time.time()
    try:
        message = bytes(json.dumps(data), "utf-8")
    except Exception() as e:
        print(e)
    header = bytes(f"{len(message):<{env.HEADER_LENGTH}}", "utf-8")
    return header + message

def decode_message(_bytes: bytes):
    message = _bytes.decode("utf-8")
    data = json.loads(message)
    data["recieved"] = time.time()
    return data

def applications_implemented():
    paths = " ".join(glob.glob("src/apps/*.py"))
    return [app.split(".")[0] for app in re.findall("[a-z]+[.]py", paths)]