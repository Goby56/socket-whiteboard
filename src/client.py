import socket as sock
import pickle, pygame, time, threading, sys, json
import env, utils
import numpy as np

if env.IP == "": env.IP = sock.gethostname()

class Client:
    def __init__(self) -> None:
        self.endpoint = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.endpoint.connect((env.IP, env.PORT))
        print(f"Joined server on {env.IP}:{env.PORT}")

        self.whiteboard = np.full(shape=(*env.DIMENSIONS, 3), fill_value=20, dtype=np.uint8)
        self.point_buffer = []

    def receive_message(self):
        header = self.endpoint.recv(env.HEADER_LENGTH) # Grab header
        msg_len = int(header)
        # is_message = True if chr(header[0]) == 0 else False
        reads_required = msg_len // env.BUFFER_SIZE + 1

        _bytes = b""
        for _ in range(reads_required):
            _bytes += self.endpoint.recv(env.BUFFER_SIZE)
        _bytes += self.endpoint.recv(msg_len % env.BUFFER_SIZE)

        # if is_message:
        #     print(_bytes.decode("utf-8"))
        #     continue
        
        self.point_buffer.extend(list(_bytes))
            # array: np.ndarray = pickle.loads(_bytes)
            # if array.shape == env.DIMENSIONS:
            #     self.whiteboard = array
            #     print("Loaded whiteboard")
            # else:
            #     self.point_stack.append(array)

    # def send_messages(self):
    #         time.sleep(1/env.UPDATE_FREQUENCY)

    #         if pygame.mouse.get_pressed()[0]:
    #             point = np.array([[230,230,230], list(pygame.mouse.get_pos()), 10], dtype=object)
    #         self.endpoint.send(utils.encode_ndarray(point))
    
# if __name__ == "__main__":
#     client_endpoint.connect((env.IP, env.PORT))
#     print(f"Joined the server on {env.IP}:{env.PORT}")

#     try:
#         listening_thread = threading.Thread(target=recieve_messages)
#         sending_thread = threading.Thread(target=send_messages)
#         listening_thread.start()
#         sending_thread.start()
#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
            
#             whiteboard = utils.add_points(whiteboard, point_stack)
#             point_stack.clear()
            
#             window.blit(utils.surface_from(whiteboard), (0,0))
#             pygame.display.update()
#             clock.tick(env.FPS)
#     except Exception as e:
#         print(e)
#     finally:
#         client_endpoint.shutdown(sock.SHUT_RDWR)
#         client_endpoint.close()
#         listening_thread.join()
#         sending_thread.join()