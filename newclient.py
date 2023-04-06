import socket
import struct
import hashlib

import page1

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # instantiate
client_socket.connect(('localhost', 5000))  # connect to the server

# message = "False"
# message = client_socket.recv(1024).decode()
#
# if message == "False":
#     print("Server connection not established")

while True:
    homepage = page1.home(client_socket)
    # while homepage == "login":
    #     pass
    # while homepage == "signup":
    #     pass



client_socket.close()  # close the connection