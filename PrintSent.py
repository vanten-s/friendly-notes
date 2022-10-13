
    

import socket
import os
import time

OpenedFile = ""
RecievedData = ""
IP = "127.0.0.1"
PORT = 42069

ADDR = (IP, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(ADDR)

s.listen(0)

while True:
    conn, addr = s.accept()
    RecievedData = conn.recv(1024).decode("utf-8")
    print(RecievedData)
    conn.close()