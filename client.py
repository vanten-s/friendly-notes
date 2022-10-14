from struct import pack
import socket
import pyray as pr

IP = "127.0.0.1"
PORT = 42069

ADDR = (IP, PORT)

notes: list = []
current_note = 0
packet = ""
class Note:
    def __init__(self, x: int, y: int, col: pr.Color) -> None:
        self.x = x
        self.y = y
        self.height = 500
        self.width = 300
        self.col = col
        self.text = ""
        self.cursorPos = (0, 0)
        self.focused = False
        notes.append(self)
        
    def set_focused(self):
        self.focused = True
    
    def reset_focused(self):
        self.focused = False
        
    def render(self):
        if self.focused: pr.draw_rectangle(self.x-5, self.y-5, self.width+10, self.height+10, pr.Color(255, 0, 0, 255))
        pr.draw_rectangle(self.x, self.y, self.width, self.height, self.col)
        
        # Try to break in the middle of a word
        text_width = pr.measure_text_ex(font, self.text, 20, 2)
        if text_width.x >= self.width-15:
            for i in range(len(self.text)):
                if pr.measure_text_ex(font, self.text[:i+1], 20, 2).x >= self.width-10:
                    final = i
                    break
       
            try:
                self.text = self.text[:final] + "\n" + self.text[final:]
        
            except UnboundLocalError:
                print("Got some weird error lol")
        
        # Try to break in beetween words
        text_width = pr.measure_text_ex(font, self.text, 20, 2)
        print(text_width.x)
        if text_width.x >= self.width-15:
            for i in range(len(self.text.split(" "))):
                if pr.measure_text_ex(font, " ".join(self.text.split()[:i+1]), 20, 2).x >= self.width-10:
                    final = i
                    break
        
            try:
                print(type(final))
                print(final)
                self.text = " ".join(self.text.split(" ")[:final] + ["\n"] + self.text.split(" ")[final:])

            except UnboundLocalError:
                print("Got some weird error lol")

        print(self.text)

        # Render Text
        height = pr.measure_text_ex(font, "abcdefghijklmnopqrstuvwxyzåäö", 20, 2).y
        current_height = 0
        for line in self.text.split("\n"):
            pr.draw_text_ex(font, line, pr.Vector2(self.x+10, self.y+10+current_height), 20, 2, pr.Color(255, 255, 255, 255))
            current_height += height
            last_line = line
            
        if self.focused:
            x = round(pr.measure_text_ex(font, last_line, 20, 2).x + self.x+10)
            current_height = round(current_height + self.y+10 - height)
            print(x)
            print(current_height)
            pr.draw_rectangle(x+1, current_height, 1, 20, pr.Color(255, 255, 255, 255))

# Init gui
pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE | pr.FLAG_WINDOW_TRANSPARENT )  # type: ignore
pr.init_window(800, 600, "notes")

font = pr.load_font_ex("roboto.ttf", 20, None, 0)

# Mainloop
# Uses only keyboard
# NO MOUSE SUPPORT
# Might add later

Note(100, 100, pr.Color(200, 100, 0, 255))
Note(500, 100, pr.Color(100, 200, 0, 255))

while not pr.window_should_close():
    
    for i in range(0, len(notes)):
        if current_note == i: notes[i].set_focused()
        else: notes[i].reset_focused()
    
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
        notes[current_note].text += char

    if pr.is_key_pressed(pr.KeyboardKey.KEY_RIGHT):
        if not pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            current_note += 1
            current_note = current_note % len(notes)
            
        else:
            notes[current_note].x += 5
            if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_ALT):
                notes[current_note].x += 10
            
    elif pr.is_key_pressed(pr.KeyboardKey.KEY_LEFT):
        if not pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            current_note -= 1
            current_note = current_note % len(notes)
            
        else:
            notes[current_note].x -= 5
            if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_ALT):
                notes[current_note].x -= 10
            
    if pr.is_key_pressed(pr.KeyboardKey.KEY_UP):
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            notes[current_note].y -= 5
            if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_ALT):
                notes[current_note].y -= 10
            
    elif pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN):
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_CONTROL):
            notes[current_note].y += 5
            if pr.is_key_down(pr.KeyboardKey.KEY_LEFT_ALT):
                notes[current_note].y += 10
   
    if pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE):
        try:
            notes[current_note].text = notes[current_note].text[:len(notes[current_note].text)-1]
            
        except:
            pass
   
    if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
        notes[current_note].text += "\n"
   
    if pr.is_key_pressed(pr.KeyboardKey.KEY_LEFT_CONTROL):
        old_packet = packet
        packet = notes[current_note].text
        if (packet != old_packet):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(ADDR)
            s.send("wtest.txt".encode("utf-8"))
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(ADDR)
            s.send(packet.encode("utf-8"))
            print(s.recv(1024).decode("utf-8"))
            s.close()
          
    pr.end_drawing()
    
pr.close_window()
