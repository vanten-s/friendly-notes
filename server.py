
    

import socket


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
            OpenedFile = open(RecievedData[1:], "r")
            conn.send(OpenedFile.read().encode("utf-8"))
        
        case "w":
            OpenedFile = open(RecievedData[1:], "w")
            conn.send("Enter text now".encode("utf-8"))
            RecievedData = ""
            while RecievedData == "":
                RecievedData = conn.recv(1024).decode("utf-8")
                print("uwu")
            
            print(RecievedData)
            OpenedFile.write(RecievedData)

        
    conn.close()