#!/usr/bin/python3

from struct import pack
import socket
import pyray as pr
import random
import json
import sys
import datetime
import os

os.system("python " + os.path.realpath(os.path.dirname(__file__)) + "/server.py &")

IP = "127.0.0.1"
PORT = 42069

ADDR = (IP, PORT)

notes: list = []
current_note = 0
packet = ""
class Note:
    def __init__(self, x: int, y: int, h: int, w: int, col: pr.Color, text: str="") -> None:
        self.x = x
        self.y = y
        self.height = h
        self.width = w
        self.col = col
        self.text = text
        self.cursorPos = (0, 0)
        self.focused = False
        notes.append(self)

    def set_focused(self):
        self.focused = True

    def reset_focused(self):
        self.focused = False

    def render(self):
        x = round(self.x)
        y = round(self.y)
        if self.focused: pr.draw_rectangle(x-5, y-5, self.width+10, self.height+10, pr.Color(255, 0, 0, 255))
        pr.draw_rectangle(x, y, self.width, self.height, self.col)

        # Render Text
        height = pr.measure_text_ex(font, "i", 20, 2).y
        current_height = 0
        for line in self.text.split("\n"):
            pr.draw_text_ex(font, line, pr.Vector2(x+10, y+10+current_height), 20, 2, pr.Color(255, 255, 255, 255))
            current_height += height
            last_line = line

        if self.focused:
            x = round(pr.measure_text_ex(font, last_line, 20, 2).x + x+10)
            current_height = round(current_height + y+10 - height)
            pr.draw_rectangle(x+1, current_height, 1, 20, pr.Color(255, 255, 255, 255))

def note_outside_box(note, width, height):
    transformed_x = note.x + note.width/2
    transformed_y = note.y + note.height/2

    recommended_x = note.x
    recommended_y = note.y

    outside = False

    if transformed_x < 0: # Note to far right
        recommended_x = 0 - note.width/2
        outside = True

    elif transformed_x > width: # Note to far left
        recommended_x = width - note.width/2
        outside = True

    if transformed_y < 0: # Note to far up
        recommended_y = 0 - note.height/2
        outside = True

    elif transformed_y > height: # Note to far down
        recommended_y = height - note.height/2
        outside = True

    return (outside, recommended_x, recommended_y) # Return combined

# Init gui
pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE | pr.FLAG_WINDOW_TRANSPARENT ) # Set flags
pr.init_window(800, 600, "notes") # Initialize window

font = pr.load_font_ex("roboto.ttf", 20, None, 0)

# Mainloop
# Uses only keyboard
# NO MOUSE SUPPORT
# Might add later

def loadNotes():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ADDR)
    s.send(f"rnotes.json".encode("utf-8"))

    try:
        notes = json.loads(s.recv(1024).decode("utf-8"))["notes"]

    except json.decoder.JSONDecodeError:
        print("Nothing valid lol")
        return None

    print(notes)

    if len(notes) <= 0:
        return None

    notesLoc = []

    for note in notes:
        x = note["x"]
        y = note["y"]
        w = note["w"]
        h = note["h"]

        col = pr.Color(note["r"], note["g"], note["b"], note["a"])
        text = note["text"]
        notesLoc.append(Note(x, y, h, w, col, text))

    return notesLoc

if not "-i" in sys.argv:
    loadNotes()

if len(notes) == 0:
    Note(100, 100, 500, 300, pr.Color(0, 0, 0, 255))

while not pr.window_should_close():
    for i in range(0, len(notes)):
        if current_note == i: notes[i].set_focused()
        else: notes[i].reset_focused()

    pr.begin_drawing()
    pr.clear_background(pr.Color(0, 0, 0, 0))
    for note in notes:
        note.render()

    char_pressed = pr.get_char_pressed()

    if char_pressed != 0:
        char = chr(char_pressed)
        notes[current_note].text += char

        if pr.measure_text_ex(font, notes[current_note].text, 20, 2).x > notes[current_note].width-20:
            notes[current_note].text = notes[current_note].text[:-1]
            notes[current_note].text += "\n" + char

    if pr.is_key_pressed(pr.KeyboardKey.KEY_RIGHT):
        if not pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            current_note += 1
            current_note = current_note % len(notes)

    elif pr.is_key_pressed(pr.KeyboardKey.KEY_LEFT):
        if not pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            current_note -= 1
            current_note = current_note % len(notes)

    if pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            notes[current_note].y += .1
            if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_ALT):
                notes[current_note].y += .5

    if pr.is_key_down(pr.KeyboardKey.KEY_UP):
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            notes[current_note].y -= .1
            if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_ALT):
                notes[current_note].y -= .5

    if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            notes[current_note].x -= .1
            if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_ALT):
                notes[current_note].x -= .5

    if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            notes[current_note].x += .1
            if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_ALT):
                notes[current_note].x += .5

    if pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE):
        try:
            notes[current_note].text = notes[current_note].text[:len(notes[current_note].text)-1]

        except:
            pass

    if pr.is_key_pressed(pr.KeyboardKey.KEY_D):
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            notes.pop(notes.index(notes[current_note]))

    if pr.is_key_pressed(pr.KeyboardKey.KEY_N):
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            Note(random.randint(0, 200)*5, random.randint(0, 200)*5, 500, 300, pr.Color(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255), 255))

    if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
        notes[current_note].text += "\n"

    if pr.is_key_pressed(pr.KeyboardKey.KEY_RIGHT_CONTROL):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR)
        s.send("q".encode("utf-8"))
        s.close()
        break


    current_note_outside_box = note_outside_box(notes[current_note], pr.get_screen_width(), pr.get_screen_height())
    print(current_note_outside_box)

    if current_note_outside_box[0]:
        notes[current_note].x = current_note_outside_box[1]
        notes[current_note].y = current_note_outside_box[2]

    if pr.is_key_pressed(pr.KeyboardKey.KEY_LEFT_CONTROL):

        obj = {"notes": [{"x": note.x, "y": note.y, "w": note.width, "h": note.height, "r": note.col.r, "g": note.col.g, "b": note.col.b, "a": note.col.a, "text": note.text} for note in notes]}

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR)
        s.send("wnotes.json".encode("utf-8"))
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR)
        s.send(json.dumps(obj=obj).encode("utf-8"))
        s.close()

        '''
        old_packet = packet
        packet = notes[current_note].text
        jsonObject = {"x": notes[current_note].x, "y": notes[current_note].y, "w": notes[current_note].width, "h": notes[current_note].height, "r": notes[current_note].col.r, "g": notes[current_note].col.g, "b": notes[current_note].col.b, "a": notes[current_note].col.a, "text": notes[current_note].text}
        jsonString = json.dumps(jsonObject)
        if (packet != old_packet):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(ADDR)
            s.send(f"wnote{current_note}.json".encode("utf-8"))
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(ADDR)
            s.send(jsonString.encode("utf-8"))
            s.close()
        '''

    pr.end_drawing()

pr.close_window()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(ADDR)
s.send("q".encode("utf-8"))
s.close()


