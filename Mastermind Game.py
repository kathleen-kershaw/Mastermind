import tkinter as tk
from tkinter import Canvas
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
BUTTON_SIZE = 24
MAX_GUESSES = 8

guesses = []
num_guesses = 0
code = []
numpad_btns = []
slot_squares = []

app = tk.Tk()
app.title("Mastermind")

canvas = Canvas(app, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

def draw_instructions():
    xt0, xt1, xrect = 40, 90, 70             # x for text and rectangle
    yt0, yt1, yrect = 15, 44, 46             # y for text and rectangle
    canvas.create_text(xt0, yt0, text="Guess the 4-digit code!  Each digit is unique.", font=("Purisa", 12), anchor="nw")
 
    canvas.create_rectangle(xrect,yrect,82,58, fill="lightgreen")
    canvas.create_text(xt1, yt1, text="Green square: Right number, correct position", font=("Purisa", 12), anchor="nw")

    canvas.create_rectangle(xrect, yrect+20,82,78, fill="yellow")
    canvas.create_text(xt1, yt1+20, text="Yellow square: Right number, wrong position", font=("Purisa", 12), anchor="nw")
 
    canvas.create_rectangle(xrect,yrect+40,82,98, fill="grey")
    canvas.create_text(xt1, yt1+40, text="Dark gray square: Number is not in the code", font=("Purisa", 12), anchor="nw")

def draw_numpad(canvas):
    xt0, yt0 = 40, 120
    button_size = 24
    canvas.create_text(xt0, yt0, text="Select 4 numbers:", font=("Purisa", 12), anchor="nw")
    bx1 = 180
    by1 = yt0
    for i in range(0,10):  
        tag = "tag" + str(i)
        bx2 = bx1 + button_size
        by2 = by1 + button_size
        # tag is the number of the button
        numpad_btns.append(canvas.create_rectangle(bx1, by1, bx2, by2, outline="black", fill="white", tags=tag))
        canvas.create_text(bx1 + button_size/2, by1 + button_size/2, text=str(i), tags=tag, font=("Purisa", 12), anchor="center")
        canvas.tag_bind(tag, '<Button-1>', on_button_click)
        bx1 = bx2 + 20

# set the backgrounds to white for the next game
def clear_numpad():
    for i in range(10):
        canvas.itemconfig(numpad_btns[i], fill='white')
    
def create_code():
    code.clear()
    while len(code) < 4:
        digit = random.randint(0,9)
        if not digit in code:
            code.append(digit)

    # for debugging - remove later
    canvas.create_text(650, 100, text=code)

def draw_guess_squares():
    bx1 = 180
    by1 = 220 + num_guesses * 30
    for i in range(0,4):  
        bx2 = bx1 + BUTTON_SIZE
        by2 = by1 + BUTTON_SIZE
        slot_squares.append(canvas.create_rectangle(bx1, by1, bx2, by2, outline="black", fill="white"))
        bx1 = bx2 + 10

def draw_guesses():
    bx1 = 180
    by1 = 220 + num_guesses * 30

    for s in range(0, len(guesses)):
        canvas.create_text(bx1 + BUTTON_SIZE/2, by1 + BUTTON_SIZE/2, text=str(guesses[s]), font=("Purisa", 12), anchor="center")
        bx1 = bx1 + BUTTON_SIZE + 10

def process_guess(slots):
    global num_guesses  

    # compare the 4 guesses in slots to the 4 items in code
    num_correct = 0
    for s in range(0, len(slots)):
        if slots[s] == code[s]:
            num_correct += 1
            canvas.itemconfig(slot_squares[s], fill='lightgreen')
            canvas.itemconfig(numpad_btns[slots[s]], fill='lightgreen')
        elif slots[s] in code:
             canvas.itemconfig(slot_squares[s], fill='yellow') 
             canvas.itemconfig(numpad_btns[slots[s]], fill='yellow')    
        else:
              canvas.itemconfig(slot_squares[s], fill='grey')
              canvas.itemconfig(numpad_btns[slots[s]], fill='grey')

    if (num_correct == 4):
        xt1 = 180 + 4 * BUTTON_SIZE + 4 * 10 + 20
        yt1 = 220 + num_guesses * 30
        canvas.create_text(xt1, yt1, text="You win!", font=("Purisa", 12), anchor="nw")
    else:
        num_guesses = num_guesses + 1 
        guesses.clear()
        slot_squares.clear()
        draw_guess_squares()
                   
# get the number that was clicked on and save it in the next slot
# after 4 numbers have been selected, see if the user guessed correctly
def on_button_click(event):
    tag = canvas.gettags("current")[0]
    tag = int(tag[3])  # strip off prefix 'tag'
    canvas.itemconfig(numpad_btns[tag], fill='lightgray')

    if (len(guesses) < 4):
        guesses.append(tag)
        print(guesses)
        draw_guesses()
    if len(guesses) == 4:
        process_guess(guesses) 
 
def main():
    canvas.pack()
    draw_instructions()
    create_code()
    draw_numpad(canvas) 
    draw_guess_squares() 
    app.mainloop()

 
if __name__ == '__main__':
    main()