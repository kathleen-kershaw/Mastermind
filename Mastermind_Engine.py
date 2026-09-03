import random

class MastermindEngine:
    def __init__(self, max_guesses=6):
        self.FEEDBACK = ["Try again", "Good start!", "Keep going!", "So close!", "You win!"]  # Feedback messages based on the number of correct digits
        self.MAX_GUESSES = max_guesses

        self.code = []
        self.history = []
        self.game_over = False
        self.message = ""
        self.reset_game()

    def reset_game(self):
        """Generates a new 4-digit unique code and clears history."""
        self.code.clear()
        while len(self.code) < 4:
            digit = random.randint(0, 9)
            if digit not in self.code:
                self.code.append(digit)
        self.history.clear()
        self.game_over = False
        self.message = ""

    def submit_guess(self, guess_list):
        """
        Evaluates a guess list (e.g., [1, 2, 3, 4]) against the secret code.
        Returns a dictionary with feedback results for each slot and game status.
        """
        if self.game_over:
            return None

        num_correct = 0
        slot_results = ['grey'] * 4
        code_copy = list(self.code)
        guess_copy = list(guess_list)

        # 1st Pass: Check for exact matches (Green)
        for i in range(4):
            if guess_copy[i] == self.code[i]:
                num_correct += 1
                slot_results[i] = 'lightgreen'
                code_copy[i] = None
                guess_copy[i] = None

        # 2nd Pass: Check for right number, wrong position (Yellow)
        for i in range(4):
            if guess_copy[i] is not None:
                if guess_copy[i] in code_copy:
                    slot_results[i] = 'yellow'
                    # Remove matched item to handle duplicates properly
                    code_copy[code_copy.index(guess_copy[i])] = None
                else:
                    slot_results[i] = 'grey'

        feedback_text = self.FEEDBACK[num_correct]

        # Record attempt in history
        attempt_record = {
            'guess': guess_list,
            'colors': slot_results,
            'feedback': feedback_text
        }
        self.history.append(attempt_record)

        # Check win/lose conditions
        if num_correct == 4:
            self.game_over = True
            self.message = "You win!"
        elif len(self.history) >= self.MAX_GUESSES:
            self.game_over = True
            self.message = f"You lose! The code was: {''.join(map(str, self.code))}"

        return attempt_record