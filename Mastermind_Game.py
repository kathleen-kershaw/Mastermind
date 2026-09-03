import tkinter as tk
from tkinter import Canvas
import random

class Mastermind_Game:

    def __init__(self):

        # Constants for the game
        self.CANVAS_WIDTH = 600
        self.CANVAS_HEIGHT = 600
        self.DEFAULT_FONT = ("Purisa", 12)  # Can't reset the default font in tkinter, so we use this for our text
        self.BUTTON_SIZE = 24      # Length and width of each button in the numpad
        self.MAX_GUESSES = 6       # Maximum number of guesses allowed
        self.GRID_X0 = 180         # x coordinate of the left edge of the guess grid
        self.GRID_Y0 = 220         # y coordinate of the top edge of the guess grid
        self.GRID_SPACING = 10     # Spacing between the rectangles in the guess grid
        self.FEEDBACK = ["Try again", "Good start!", "Keep going!", "So close!", "You win!"]  # Feedback messages based on the number of correct digits

        self.numpad_btns = []      # List to hold the buttons for the digits 0 - 9
        self.current_guess = []    # The current guess being built by the user, a list of 4 digits 
        self.attempt_num = 0      # Number of attempts made by the user
        self.code = []             # The code to be guessed, a list of 4 unique digits

        # List to hold the grid for the guesses.  We will change rectangle colors to indicate correctness
        self.guess_grid = [[0 for _ in range(4)] for _ in range(self.MAX_GUESSES)] 

        # Setup main window
        self.app = tk.Tk()
        self.app.title("Mastermind")

        self.canvas = Canvas(self.app, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.pack()

        # Build UI elements
        self.my_button = tk.Button(self.app, text="Play Again!", command=self.play_game, font=self.DEFAULT_FONT, width=10, height=2)
        self.canvas.create_window(250, 550, window=self.my_button) 

        self.draw_instructions()
        self.draw_numpad() 
        self.draw_guess_grid() 

        # Start the game
        self.play_game()        

    # Add the game instructions to the canvas
    def draw_instructions(self):
            xt0, xt1, xrect1, xrect2 = 40, 90, 70, 82            # x for text and rectangle
            yt0, yt1, yrect1, yrect2 = 15, 44, 46, 58            # y for text and rectangle
        
            self.canvas.create_text(xt0, yt0, text="Guess the 4-digit code!  Each digit is unique.", font=self.DEFAULT_FONT, anchor="nw")
        
            self.canvas.create_rectangle(xrect1, yrect1, xrect2, yrect2, fill="lightgreen")
            self.canvas.create_text(xt1, yt1, text="Green square: Right number, correct position", font=self.DEFAULT_FONT, anchor="nw")

            self.canvas.create_rectangle(xrect1, yrect1+20, xrect2, yrect2+20, fill="yellow")
            self.canvas.create_text(xt1, yt1+20, text="Yellow square: Right number, wrong position", font=self.DEFAULT_FONT, anchor="nw")
        
            self.canvas.create_rectangle(xrect1, yrect1+40, xrect2, yrect2+40, fill="grey")
            self.canvas.create_text(xt1, yt1+40, text="Dark gray square: Number is not in the code", font=self.DEFAULT_FONT, anchor="nw")

            self.canvas.create_text(xt0, yt1 + 70, text="Click on the keypad below to select your guess:", font=self.DEFAULT_FONT, anchor="nw")
            self.canvas.create_text(xt0, yt1 + 150, text="You have up to " + str(self.MAX_GUESSES) + " guesses:", font=self.DEFAULT_FONT, anchor="nw")

        # Draw the numpad with buttons for digits 0-9
 
    def draw_numpad(self):
            bx1 = 100
            by1 = 150
            self.canvas.create_rectangle(bx1 - 10, by1 - 10, bx1 + 435, by1 + 32, outline="black", fill="lightblue")

            for i in range(0,10):  
                tag = "tag" + str(i)  # tag is the digit corresponding to the button, with the prefix 'tag'
                bx2 = bx1 + self.BUTTON_SIZE
                by2 = by1 + self.BUTTON_SIZE
                self.numpad_btns.append(self.canvas.create_rectangle(bx1, by1, bx2, by2, outline="black", fill="white", tags=tag))
                self.canvas.create_text(bx1 + self.BUTTON_SIZE/2, by1 + self.BUTTON_SIZE/2, text=str(i), tags=tag, font=self.DEFAULT_FONT, anchor="center")
                self.canvas.tag_bind(tag, '<Button-1>', self.on_button_click)
                bx1 = bx2 + 20

        # Set the backgrounds to white for the next game

    def clear_numpad(self):
        for i in range(10):
                self.canvas.itemconfig(self.numpad_btns[i], fill='white')

    # Clear the guess grid and reset the number of attempts
    def clear_guess_grid(self):
            self.attempt_num = 0  # Reset the number of attempts
            for row in range(0, self.MAX_GUESSES):
                for col in range(0, 4):
                    self.canvas.itemconfig(self.guess_grid[row][col], fill='white')
            self.current_guess.clear()
            self.canvas.delete("guess")     # Remove previous guesses from the canvas
            self.canvas.delete("feedback")  # Remove previous feedback from the canvas

        # Create a new code of 4 unique digits for the user to guess   
   
    def create_code(self):
            self.code.clear()
            while len(self.code) < 4:
                digit = random.randint(0,9)
                if not digit in self.code:
                    self.code.append(digit)
        #    print(code)  # Uncomment this line to see the code in the console for testing purposes

        # Draw the grid for the guesses

    def draw_guess_grid(self):
        for row in range(0, self.MAX_GUESSES):
            bx1 = self.GRID_X0
            by1 = self.GRID_Y0 + row * 30
            for col in range(0,4):  
                bx2 = bx1 + self.BUTTON_SIZE
                by2 = by1 + self.BUTTON_SIZE
                self.guess_grid[row][col] = self.canvas.create_rectangle(bx1, by1, bx2, by2, outline="black", fill="white")
                bx1 = bx2 + self.GRID_SPACING

    # Draw a digit in the specified slot position in the guess grid
    def draw_digit(self, slot_position, digit):
        dx = self.GRID_X0 + self.BUTTON_SIZE/2 + (self.BUTTON_SIZE + self.GRID_SPACING) * slot_position
        dy = self.GRID_Y0 + self.attempt_num * 30

        self.canvas.create_text(dx, dy + self.BUTTON_SIZE/2, text=str(digit), font=self.DEFAULT_FONT, anchor="center", tags="guess")

    # Compare the 4 guesses in slots to the 4 items in code and provide feedback.
    def process_guess(self, slots):
        global attempt_num  

        num_correct = 0
        for s in range(0, len(slots)):
            if slots[s] == self.code[s]:
                num_correct += 1
                self.canvas.itemconfig(self.guess_grid[self.attempt_num][s], fill='lightgreen')
                self.canvas.itemconfig(self.numpad_btns[slots[s]], fill='lightgreen')
            elif slots[s] in self.code:
                self.canvas.itemconfig(self.guess_grid[self.attempt_num][s], fill='yellow') 
                self.canvas.itemconfig(self.numpad_btns[slots[s]], fill='yellow')    
            else:
                self.canvas.itemconfig(self.guess_grid[self.attempt_num][s], fill='grey')
                self.canvas.itemconfig(self.numpad_btns[slots[s]], fill='grey')

        # Location for feedback text
        xt1 = self.GRID_X0 + 4 * self.BUTTON_SIZE + 4 * 10 + 20
        yt1 = self.GRID_Y0 + self.attempt_num * 30

        if self.attempt_num <= self.MAX_GUESSES - 1:
            attempt_feedback = self.canvas.create_text(xt1, yt1, text=self.FEEDBACK[num_correct], font=self.DEFAULT_FONT, anchor="nw", tag="feedback")
    
        if (num_correct < 4):
            self.attempt_num = self.attempt_num + 1 
            self.current_guess.clear()
            if (self.attempt_num == self.MAX_GUESSES):
                self.canvas.delete(attempt_feedback)
                self.canvas.create_text(xt1, yt1, text="You lose! The code was: " + ''.join(map(str, self.code)), font=self.DEFAULT_FONT, anchor="nw", tag="feedback")
                            
    # User clicked on a button in the numpad
    def on_button_click(self, event):
        # Get the number that was clicked on and save it in the next guess slot.
        tag = self.canvas.gettags("current")[0]
        digit = int(tag[3])  # strip off prefix 'tag'
        # Gray out the button that was clicked.
        self.canvas.itemconfig(self.numpad_btns[digit], fill='lightgray')

        if (len(self.current_guess) < 4):
            self.current_guess.append(digit)
            self.draw_digit(len(self.current_guess)-1, digit)

        # After 4 numbers have been selected, see if the user guessed correctly
        if len(self.current_guess) == 4: 
            self.process_guess(self.current_guess) 

    # Function to reset the game and start a new one
    def play_game(self):
        self.clear_numpad()
        self.clear_guess_grid()
        self.create_code()

    def run(self):
        self.app.mainloop()

if __name__ == '__main__':
    game_app = Mastermind_Game()
    game_app.run()