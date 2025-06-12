import tkinter as tk
from tkinter import Canvas
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
DEFAULT_FONT = ("Purisa", 12)  # Can't reset the default font in tkinter, so we use this for our text

# Constants for the game
BUTTON_SIZE = 24        # Length and width of each button in the numpad
MAX_GUESSES = 8         # Maximum number of guesses allowed

numpad_btns = []        # List to hold the buttons for the digits 0 - 9

guesses = []
num_guesses = 0
code = []
slot_squares = []

app = tk.Tk()
app.title("Mastermind")

canvas = Canvas(app, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

def draw_instructions():
    xt0, xt1, xrect1, xrect2 = 40, 90, 70, 82            # x for text and rectangle
    yt0, yt1, yrect1, yrect2 = 15, 44, 46, 58            # y for text and rectangle
 
    canvas.create_text(xt0, yt0, text="Guess the 4-digit code!  Each digit is unique.", font=DEFAULT_FONT, anchor="nw")
 
    canvas.create_rectangle(xrect1, yrect1, xrect2, yrect2, fill="lightgreen")
    canvas.create_text(xt1, yt1, text="Green square: Right number, correct position", font=DEFAULT_FONT, anchor="nw")

    canvas.create_rectangle(xrect1, yrect1+20, xrect2, yrect2+20, fill="yellow")
    canvas.create_text(xt1, yt1+20, text="Yellow square: Right number, wrong position", font=DEFAULT_FONT, anchor="nw")
 
    canvas.create_rectangle(xrect1, yrect1+40, xrect2, yrect2+40, fill="grey")
    canvas.create_text(xt1, yt1+40, text="Dark gray square: Number is not in the code", font=DEFAULT_FONT, anchor="nw")

    canvas.create_text(xt0, yt1 + 70, text="Click on the numbers below to select your guess:", font=DEFAULT_FONT, anchor="nw")
    canvas.create_text(xt0, yt1 + 140, text="You have up to " + str(MAX_GUESSES) + " guesses:", font=DEFAULT_FONT, anchor="nw")

def draw_numpad():
    bx1 = 140
    by1 = 140
    for i in range(0,10):  
        tag = "tag" + str(i)
        bx2 = bx1 + BUTTON_SIZE
        by2 = by1 + BUTTON_SIZE
        # tag is the number of the button
        numpad_btns.append(canvas.create_rectangle(bx1, by1, bx2, by2, outline="black", fill="white", tags=tag))
        canvas.create_text(bx1 + BUTTON_SIZE/2, by1 + BUTTON_SIZE/2, text=str(i), tags=tag, font=DEFAULT_FONT, anchor="center")
        canvas.tag_bind(tag, '<Button-1>', on_button_click)
        bx1 = bx2 + 20

# set the backgrounds to white for the next game
def clear_numpad():
    for i in range(10):
        canvas.itemconfig(numpad_btns[i], fill='white')

# Create a new code of 4 unique digits for the user to guess   
def create_code():
    code.clear()
    while len(code) < 4:
        digit = random.randint(0,9)
        if not digit in code:
            code.append(digit)

def draw_guess_squares():
    bx1 = 180
    by1 = 220 + num_guesses * 30
    for i in range(0,4):  
        bx2 = bx1 + BUTTON_SIZE
        by2 = by1 + BUTTON_SIZE
        slot_squares.append(canvas.create_rectangle(bx1, by1, bx2, by2, outline="black", fill="white", tags="slot"))
        bx1 = bx2 + 10

def draw_guesses():
    bx1 = 180
    by1 = 220 + num_guesses * 30

    for s in range(0, len(guesses)):
        canvas.create_text(bx1 + BUTTON_SIZE/2, by1 + BUTTON_SIZE/2, text=str(guesses[s]), font=DEFAULT_FONT, anchor="center")
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
        canvas.create_text(xt1, yt1, text="You win!", font=DEFAULT_FONT, anchor="nw")
    else:
        num_guesses = num_guesses + 1 
        guesses.clear()
        slot_squares.clear()
        draw_guess_squares()
                   
# Get the number that was clicked on and save it in the next guess slot.
# Gray out the button that was clicked.
# After 4 numbers have been selected, see if the user guessed correctly
def on_button_click(event):
    tag = canvas.gettags("current")[0]
    digit = int(tag[3])  # strip off prefix 'tag'
    canvas.itemconfig(numpad_btns[digit], fill='lightgray')

    if (len(guesses) < 4):
        guesses.append(digit)
        draw_guesses()
    if len(guesses) == 4:
        process_guess(guesses) 

def play_game():
    create_code()
    clear_numpad()
#    canvas.delete("slot")  # clear the guess squares
    draw_guess_squares() 

def main():
    canvas.pack()
 #   my_button = tk.Button(app, text="Play Again!", command=play_game, font=DEFAULT_FONT, width=10, height=2)
 #   canvas.create_window(400, 550, window=my_button) 

    draw_instructions()
    draw_numpad() 
    play_game()

    app.mainloop()

if __name__ == '__main__':
    main()