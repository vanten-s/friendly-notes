
import socket
import os
import time

OpenedFile = ""
recieved_data = ""
IP = "127.0.0.1"
PORT = 42069

ADDR = (IP, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(ADDR)

s.listen(0)

print("Listening")

# Server Mainloop
while True:
    conn, addr = s.accept()
    recieved_data = conn.recv(1024).decode("utf-8")
    print(recieved_data)


    match_thing = recieved_data[0]
    if True:
        # read specified file
        # how to use: send "r<filename.extension>"
        if match_thing == "r":
            if os.path.exists(recieved_data[1:]):
                with open(recieved_data[1:], "r") as OpenedFile:
                    conn.send(OpenedFile.read().encode("utf-8"))
                    print("read")
                    OpenedFile.close()
            else:
                conn.send(f"File doesn't exist {recieved_data[1:]}".encode("utf-8"))
                print("File doesn't exist")
                
        # write to specified file
        # how to use: send w<filename.extension>
        # then send another package with the data
        elif match_thing == "w":
            with open(recieved_data[1:], "w") as OpenedFile:
                conn.send("Send".encode("utf-8"))
                uwu = ""
            
                # reset connection to recieve another package
                # yes, cursed indeed
                conn.close()
                conn, addr = s.accept()
                recieved_data = conn.recv(1024).decode("utf-8")
            
                # write to file
                OpenedFile.write(recieved_data)
                OpenedFile.close()
                print("written")
                conn.send("Written".encode("utf-8"))
        
        # format specified file
        # how to use: send f<filename.extension>
        elif match_thing == "f":
            if os.path.exists(recieved_data[1:]):
                os.remove(recieved_data[1:])
                conn.send("Deleted".encode("utf-8"))
                print("deleted")
            else:
                conn.send("File doesn't exist".encode("utf-8"))
                print("File doesn't exist")
    conn.close()
    if (recieved_data[0] == "q"):
        break
    
