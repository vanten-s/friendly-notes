
    

import socket
import time

OpenedFile = ""
RecievedData = ""
IP = "127.0.0.2"
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
                print("Sent -> " + OpenedFile.read())
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
                print("CLOSED")
            
            
        
        
        
    conn.close()