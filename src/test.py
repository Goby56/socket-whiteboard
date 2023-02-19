from timeit import default_timer
import random, importlib, uuid, json, time
import tkinter as tk
from PIL import Image, ImageDraw

def timer(func):
    def wrapper(*args, **kwargs):
        t0 = default_timer()
        rv = func(*args, **kwargs)
        print(default_timer() - t0)
        return rv
    return wrapper

@timer
def pause(tick_rate):
    for i in range(tick_rate):
        print(i)
        print(1/tick_rate)
        time.sleep(1/tick_rate)

pause(20)





# img = Image.new("RGB", (100, 100))
# draw = ImageDraw.Draw(img)
# draw.text((0,0), "Per")
# # img.show()
# by = list(img.tobytes()[:10])
# print(by)
# print(len(by))

# draw = ImageDraw.Draw(img)
# draw.text((0,0), "Per")
# by = img.tobytes()
# print(len(by))
# st = str(by)
# print(len(st))

# data = {
#     "point": {
#         "pos": [345, 353],
#         "brush_down": True,
#         "size": 10,
#         "color": [123,232,121]
#     },
#     "canvas": st
# }
# data_by = bytes(json.dumps(data), "utf-8")
# print(len(data_by))

# img = Image.frombytes("RGB", (511, 448), by)
# img.show()

# for i in range(len(by)):
#     if random.randint(0, 1):
#         by[i] = 
# img = Image.frombytes("RGB", (200,200), by)
# img.show()




# print(uuid.uuid4().bytes)
# module = importlib.import_module("apps.canvas")
# print(module.__dict__["CanvasClient"])
# print("upper case".capitalize())
# t = tuple(random.randint(0, 255) for _ in range(3))
# print(t)
# import timeit, time

# t0 = timeit.default_timer()
# time.time()
# t1 = timeit.default_timer()
# print(t1 - t0)

# t0 = time.time()
# timeit.default_timer()
# timeit.default_timer()
# t1 = time.time()
# print(t1 - t0)

# times = []
# i = 0
# pre_t = timer()
# print(pre_t)
# print(timer())
# while True:
#     # if i > 100:
#     #     break
#     delta = timer() - pre_t
#     if delta > 1/20:
#         pre_t = timer()
#         print(delta*20)
        # i += 1

# print(times)


              

