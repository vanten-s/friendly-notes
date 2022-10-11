
import socket
import pyray as pr

# Connect to server 
IP = "127.0.0.1"
PORT = 42069

ADDR = (IP, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDR)

# Init gui
pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE | pr.FLAG_WINDOW_TRANSPARENT )
pr.init_window(800, 600, "notes")

# Mainloop
# Uses only keyboard
# NO MOUSE SUPPORT
# Might add later

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.Color(0, 0, 0, 0))
    # pr.draw_rectangle(37, 0, 25, 100, pr.Color(255, 255, 255, 255))
    # pr.draw_rectangle(0, 37, 100, 25, pr.Color(255, 255, 255, 255))
    pr.end_drawing()
    
pr.close_window()
