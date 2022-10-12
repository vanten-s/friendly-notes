
import socket
import pyray as pr
from pyray import KeyboardKey as kk
import os

# Connect to server 
# IP = "127.0.0.1"
# PORT = 42069

# ADDR = (IP, PORT)

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(ADDR)

notes = []
currentNote = 0

class Note:
    def __init__(self, x: int, y: int, col: pr.Color) -> None:
        self.x = x
        self.y = y
        self.height = 500
        self.width = 300
        self.col = col
        self.text = ""
        self.cursorPos = (0, 0)
        notes.append(self)
        
    def render(self):
        pr.draw_rectangle(self.x, self.y, self.width, self.height, self.col)
        pr.draw_text_ex(font, self.text, pr.Vector2(self.x+10, self.y+10), 20, 2, pr.Color(255, 255, 255, 255))
        pr.draw_rectangle(self.cursorPos[0]*12, self.cursorPos[1]*12, 10, 20, pr.Color(0, 0, 0, 0)) 

# Init gui
pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE | pr.FLAG_WINDOW_TRANSPARENT )  # type: ignore
pr.init_window(800, 600, "notes")

font = pr.load_font_ex("roboto.ttf", 20, None, 0)

# Mainloop
# Uses only keyboard
# NO MOUSE SUPPORT
# Might add later

Note(100, 100, pr.Color(200, 100, 0, 255))

while not pr.window_should_close():
    pr.begin_drawing()
    # TODO
    # ADD KEYBOARD SUPPORT
    # ACTUALLY USE THE SERVER
    pr.clear_background(pr.Color(0, 0, 0, 0))
    # pr.draw_rectangle(37, 0, 25, 100, pr.Color(255, 255, 255, 255))
    # pr.draw_rectangle(0, 37, 100, 25, pr.Color(255, 255, 255, 255))
    for note in notes:
        note.render()   
    
    char_pressed = pr.get_char_pressed()
    
    if char_pressed != 0:
        print(chr(char_pressed))
        char = chr(char_pressed)
        notes[currentNote].text += char
    
    pr.end_drawing()
    
pr.close_window()
