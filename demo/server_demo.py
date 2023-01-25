import socket as s
import time
import pickle





HEADER_SIZE = 10

endpoint: s.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
endpoint.bind((s.gethostname(), 6969))
endpoint.listen(10)

# while True:
#     client_endpoint, adress = endpoint.accept()
#     print(f"Connection from {adress} has been made.")

#     dct = {
#         "red": (255, 0, 0),
#         "green": (0, 255, 0),
#         "blue": (0, 0, 255)
#     }
#     msg = pickle.dumps(dct)
#     msg = bytes(f"{len(msg):<{HEADER_SIZE}}", "utf-8") + msg
#     client_endpoint.send(msg)

clients = {}

while True:
    client_endpoint, address = endpoint.accept()
    clients[address] = client_endpoint
    print(f"Connection from {address} has been made.")

    msg = "The empire is pretty chill."
    msg = f"{len(msg):<{HEADER_SIZE}}" + msg
    client_endpoint.send(bytes(msg, "utf-8"))
    
    if int(time.time()) % 2 == 0:
        for address, client_endpoint in clients.items():
            msg = "Status check"
            msg = f"{len(msg):<{HEADER_SIZE}}" + msg
            client_endpoint.send(bytes(msg, "utf-8"))
        
            print(f"Message sent to {address}")


    # while True:
    #     time.sleep(3)

    #     msg = "Status check"
    #     msg = f"{len(msg):<{HEADER_SIZE}}" + msg
    #     client_endpoint.send(bytes(msg, "utf-8"))
        
    #     print(f"Message sent to {adress}")

        