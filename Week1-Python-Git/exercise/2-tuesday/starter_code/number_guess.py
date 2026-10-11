"""
number_guess.py - Day 2 exercise, Part 2: the number-guessing game.

Read first: "Break and Continue Statements" (section 2.5, the guessing-game
skeleton), "Loops: for and while", "Conditional Statements: if, elif, else",
"Input and Output Operations".

HOW TO RUN (play it yourself)
    python3 number_guess.py          (Windows: python number_guess.py)

HOW THE SELF-CHECK TESTS IT (no typing needed)
    check_exercise.py makes a temporary copy of this file, changes the two
    constants below (SECRET_NUMBER and MAX_ATTEMPTS), feeds it a scripted list
    of guesses and reads what it prints. So:
      - keep the constant names SECRET_NUMBER and MAX_ATTEMPTS, each on its own line
      - print the messages EXACTLY as the README specifies
"""

# ---- Settings (provided; do not rename) ------------------------------------
SECRET_NUMBER = 42      # fixed on purpose so the game can be tested
MAX_ATTEMPTS = 7        # a guess that counts uses up one attempt
MIN_NUMBER = 1
MAX_NUMBER = 100

# ---- State (provided) -------------------------------------------------------
attempts = 0            # how many VALID guesses so far
result = "NONE"         # must end as "WIN", "LOSE" or "QUIT"

print(f"Guess the number between {MIN_NUMBER} and {MAX_NUMBER}. "
      f"You have {MAX_ATTEMPTS} attempts. Type q to quit.")

# ---- TODO 1: the game loop ---------------------------------------------------
# Build a `while True:` loop. Inside it, in THIS order (order matters!):
#   a) read the answer:  answer = input("Guess (1-100): ").strip()
#   b) if answer is "q" (any case): print "You quit. The number was <SECRET_NUMBER>."
#        set result = "QUIT"  and  break
#   c) if answer is not all digits (.isdigit()): print
#        "Invalid input: please type a whole number."  and  continue
#        (does NOT use up an attempt)
#   d) convert with int(); if outside MIN_NUMBER..MAX_NUMBER: print
#        "Out of range: choose a number from 1 to 100."  and  continue
#        (does NOT use up an attempt)
#   e) now it is a real guess:  attempts += 1
#   f) if/elif/else:  "Too low"  /  "Too high"  /
#        "Correct! You needed <attempts> attempts."  -> result = "WIN" and break
#   g) if attempts >= MAX_ATTEMPTS (and the guess was wrong): print
#        "Out of attempts! The number was <SECRET_NUMBER>."
#        result = "LOSE" and break
# Commit when the loop works for a WIN. Then commit again after LOSE/QUIT.

# ---- Final line (provided; the checker reads this) --------------------------
print(f"RESULT: {result} attempts={attempts}")
