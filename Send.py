

import socket


IP = "127.0.0.1"
PORT = 42069

ADDR = (IP, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDR)
while True:
    Packet = input("-> ")

    s.send(Packet.encode("utf-8"))
    print(s.recv(1024))

s.close()