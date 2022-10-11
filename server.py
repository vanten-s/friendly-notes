

import socket


OpenedFile = ""
RecievedData = ""
IP = "127.0.0.7"
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
            OpenedFile = open(RecievedData[1:9], "r")
            conn.send(OpenedFile.read().encode("utf-8"))
        
    
        
    conn.close()
    