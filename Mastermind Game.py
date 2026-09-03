import tkinter as tk
from tkinter import Canvas
import random

# Constants for the game

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
DEFAULT_FONT = ("Purisa", 12)  # Can't reset the default font in tkinter, so we use this for our text
BUTTON_SIZE = 24      # Length and width of each button in the numpad
MAX_GUESSES = 6       # Maximum number of guesses allowed
GRID_X0 = 180         # x coordinate of the left edge of the guess grid
GRID_Y0 = 220         # y coordinate of the top edge of the guess grid
GRID_SPACING = 10     # Spacing between the rectangles in the guess grid
FEEDBACK = ["Try again", "Good start!", "Keep going!", "So close!", "You win!"]  # Feedback messages based on the number of correct digits

numpad_btns = []      # List to hold the buttons for the digits 0 - 9
current_guess = []    # The current guess being built by the user, a list of 4 digits 
num_attempts = 0      # Number of attempts made by the user
code = []             # The code to be guessed, a list of 4 unique digits

# List to hold the grid for the guesses.  We will change rectangle colors to indicate correctness
guess_grid = [[0 for _ in range(4)] for _ in range(MAX_GUESSES)] 


app = tk.Tk()
app.title("Mastermind")

canvas = Canvas(app, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

# Add the game instructions to the canvas
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

    canvas.create_text(xt0, yt1 + 70, text="Click on the keypad below to select your guess:", font=DEFAULT_FONT, anchor="nw")
    canvas.create_text(xt0, yt1 + 150, text="You have up to " + str(MAX_GUESSES) + " guesses:", font=DEFAULT_FONT, anchor="nw")

# Draw the numpad with buttons for digits 0-9
def draw_numpad():
    bx1 = 100
    by1 = 150
    canvas.create_rectangle(bx1 - 10, by1 - 10, bx1 + 435, by1 + 32, outline="black", fill="lightblue")

    for i in range(0,10):  
        tag = "tag" + str(i)  # tag is the digit corresponding to the button, with the prefix 'tag'
        bx2 = bx1 + BUTTON_SIZE
        by2 = by1 + BUTTON_SIZE
        numpad_btns.append(canvas.create_rectangle(bx1, by1, bx2, by2, outline="black", fill="white", tags=tag))
        canvas.create_text(bx1 + BUTTON_SIZE/2, by1 + BUTTON_SIZE/2, text=str(i), tags=tag, font=DEFAULT_FONT, anchor="center")
        canvas.tag_bind(tag, '<Button-1>', on_button_click)
        bx1 = bx2 + 20

# Set the backgrounds to white for the next game
def clear_numpad():
    for i in range(10):
        canvas.itemconfig(numpad_btns[i], fill='white')

# Clear the guess grid and reset the number of attempts
def clear_guess_grid():
    global num_attempts
    num_attempts = 0  # Reset the number of attempts
    for row in range(0, MAX_GUESSES):
        for col in range(0, 4):
            canvas.itemconfig(guess_grid[row][col], fill='white')
    current_guess.clear()
    canvas.delete("guess")     # Remove previous guesses from the canvas
    canvas.delete("feedback")  # Remove previous feedback from the canvas

# Create a new code of 4 unique digits for the user to guess   
def create_code():
    code.clear()
    while len(code) < 4:
        digit = random.randint(0,9)
        if not digit in code:
            code.append(digit)

# Draw the grid for the guesses
def draw_guess_grid():
     for row in range(0, MAX_GUESSES):
        bx1 = GRID_X0
        by1 = GRID_Y0 + row * 30
        for col in range(0,4):  
            bx2 = bx1 + BUTTON_SIZE
            by2 = by1 + BUTTON_SIZE
            guess_grid[row][col] = canvas.create_rectangle(bx1, by1, bx2, by2, outline="black", fill="white")
            bx1 = bx2 + GRID_SPACING

# Draw a digit in the specified slot position in the guess grid
def draw_digit(slot_position, digit):
    dx = GRID_X0 + BUTTON_SIZE/2 + (BUTTON_SIZE + GRID_SPACING) * slot_position
    dy = GRID_Y0 + num_attempts * 30

    canvas.create_text(dx, dy + BUTTON_SIZE/2, text=str(digit), font=DEFAULT_FONT, anchor="center", tags="guess")

# Compare the 4 guesses in slots to the 4 items in code and provide feedback.
def process_guess(slots):
    global num_attempts  

    num_correct = 0
    for s in range(0, len(slots)):
        if slots[s] == code[s]:
            num_correct += 1
            canvas.itemconfig(guess_grid[num_attempts][s], fill='lightgreen')
            canvas.itemconfig(numpad_btns[slots[s]], fill='lightgreen')
        elif slots[s] in code:
             canvas.itemconfig(guess_grid[num_attempts][s], fill='yellow') 
             canvas.itemconfig(numpad_btns[slots[s]], fill='yellow')    
        else:
              canvas.itemconfig(guess_grid[num_attempts][s], fill='grey')
              canvas.itemconfig(numpad_btns[slots[s]], fill='grey')

    # Location for feedback text
    xt1 = GRID_X0 + 4 * BUTTON_SIZE + 4 * 10 + 20
    yt1 = GRID_Y0 + num_attempts * 30

    if num_attempts < MAX_GUESSES -1:
        canvas.create_text(xt1, yt1, text=FEEDBACK[num_correct], font=DEFAULT_FONT, anchor="nw", tag="feedback")
 
    if (num_correct < 4):
        num_attempts = num_attempts + 1 
        current_guess.clear()
        if (num_attempts >= MAX_GUESSES):
             canvas.create_text(xt1, yt1, text="You lose! The code was: " + ''.join(map(str, code)), font=DEFAULT_FONT, anchor="nw", tag="feedback")
                    
# User clicked on a button in the numpad
def on_button_click(event):
    # Get the number that was clicked on and save it in the next guess slot.
    tag = canvas.gettags("current")[0]
    digit = int(tag[3])  # strip off prefix 'tag'
    # Gray out the button that was clicked.
    canvas.itemconfig(numpad_btns[digit], fill='lightgray')

    if (len(current_guess) < 4):
        current_guess.append(digit)
        draw_digit(len(current_guess)-1, digit)

    # After 4 numbers have been selected, see if the user guessed correctly
    if len(current_guess) == 4: 
        process_guess(current_guess) 

# Function to reset the game and start a new one
def play_game():
    clear_numpad()
    clear_guess_grid()
    create_code()

# Mastermind game!
def main():
    canvas.pack()
    my_button = tk.Button(app, text="Play Again!", command=play_game, font=DEFAULT_FONT, width=10, height=2)
    canvas.create_window(250, 550, window=my_button) 

    draw_instructions()
    draw_numpad() 
    draw_guess_grid() 

    play_game()

    app.mainloop()

if __name__ == '__main__':
    main()