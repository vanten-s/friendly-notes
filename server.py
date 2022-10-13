
    

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





# Server Mainloop
while True:
    conn, addr = s.accept()
    RecievedData = conn.recv(1024).decode("utf-8")
    print(RecievedData)



    match RecievedData[0]:
        case "r":
            if os.path.exists(RecievedData[1:]):
                with open(RecievedData[1:], "r") as OpenedFile:
                    conn.send(OpenedFile.read().encode("utf-8"))
                    print("read")
                    OpenedFile.close()
            else:
                conn.send("File doesn't exist".encode("utf-8"))
                print("File doesn't exist")
                
                
        case "w":
            if os.path.exists(RecievedData[1:]):
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
            else:
                conn.send("File doesn't exist".encode("utf-8"))
                print("File doesn't exist")
            
        case "x":
            if os.path.exists(RecievedData[1:]):
                conn.send("File already exists".encode("utf-8"))
                print("File already exists")
            else:
                with open(RecievedData[1:], "x") as OpenedFile:
                    OpenedFile.close()
                    conn.send("Created".encode("utf-8"))
                    print("created")
        
        case "f":
            if os.path.exists(RecievedData[1:]):
                os.remove(RecievedData[1:])
                conn.send("Deleted".encode("utf-8"))
                print("deleted")
            else:
                conn.send("File doesn't exist".encode("utf-8"))
                print("File doesn't exist")
    conn.close()
    if (RecievedData[0] == "q"):
        break
    