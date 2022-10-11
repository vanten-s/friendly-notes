
    

import socket
import time

OpenedFile = ""
RecievedData = ""
IP = "127.0.0.1"
PORT = 42069

ADDR = (IP, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

s.listen(0)





# Server Mainloop
while True:
    conn, addr = s.accept()
    RecievedData = conn.recv(1024).decode("utf-8")




    match RecievedData[0]:
        case "r":
            with open(RecievedData[1:], "r") as OpenedFile:
                conn.send(OpenedFile.read().encode("utf-8"))
                print("read")
                OpenedFile.close()
        
        case "w":
            with open(RecievedData[1:], "w") as OpenedFile:
                conn.send("Send".encode("utf-8"))
                uwu = ""
                conn.close()
                conn, addr = s.accept()
                RecievedData = conn.recv(1024).decode("utf-8")
                
                OpenedFile.write(RecievedData)
                OpenedFile.close()
                print("written")
                conn.send("Written".encode("utf-8"))
            
        case "x":
            with open(RecievedData[1:], "x") as OpenedFile:
                OpenedFile.close()
                conn.send("Created".encode("utf-8"))
                print("created")
        
        
        
    conn.close()