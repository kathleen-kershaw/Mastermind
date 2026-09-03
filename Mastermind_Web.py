import streamlit as st
from Mastermind_Engine import MastermindEngine

st.title("Mastermind Web Edition")
st.write("Guess the 4-digit code (each digit is unique, 0–9).")

# Initialize the game engine in session state
if 'engine' not in st.session_state:
    st.session_state.engine = MastermindEngine()

engine = st.session_state.engine

# Game play area
if not engine.game_over:
    raw_guess = st.text_input("Enter your 4-digit guess:", max_chars=4, key="guess_input")
    
    if st.button("Submit Guess"):
        if len(raw_guess) == 4 and raw_guess.isdigit():
            guess_list = [int(char) for char in raw_guess]
            engine.submit_guess(guess_list)
            st.rerun()
        else:
            st.error("Please enter exactly 4 numbers (e.g., 1234).")

# Display past attempts history with detailed feedback
if engine.history:
    st.subheader("Guess History:")
    
    for i, entry in enumerate(engine.history, 1):
        guess_str = "".join(map(str, entry['guess']))
        
        # Map your engine's color terms to simple emoji blocks for each slot
        emoji_map = {
            'lightgreen': '🟩',
            'yellow': '🟨',
            'grey': '⬜'
        }
        
        # Build a string of emojis matching the 4 slots
        slots_display = "".join([emoji_map[color] for color in entry['colors']])
        
        # Display the guess, the slot emojis, and the feedback text
        st.write(f"**#{i}: {guess_str}** &nbsp;&nbsp; {slots_display} &nbsp;&nbsp; *{entry['feedback']}*")

# Show win/lose message and restart button
if engine.game_over:
    st.subheader(engine.message)
    if st.button("Play Again!"):
        engine.reset_game()
        st.rerun()