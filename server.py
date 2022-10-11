

import socket


OpenedFile = ""
RecievedData = ""
IP = "127.0.0.6"
PORT = 42069

ADDR = (IP, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

s.listen(0)





# Server Mainloop
while True:
    conn, addr = s.accept()
    RecievedData = conn.recv(1024).decode("utf-8")




    
    if RecievedData[0] == "r":

        OpenedFile = open("test.txt", "r")
        packet = OpenedFile.read()
        conn.send(packet.encode("utf-8"))

    conn.close()
    