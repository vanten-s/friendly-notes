
import socket

IP = "127.0.0.1"
PORT = 42069

ADDR = (IP, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

s.listen(0)

# Server Mainloop
while True:
    conn, addr = s.accept()
    conn.recv(1024)
    conn.send("Bye Bye!".encode("utf-8"))
    conn.close()
