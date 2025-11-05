

import random


import string


import os


import sys


from typing import List, Tuple, Dict, Any, Optional


def get_password_with_asterisks(prompt="Password: "):


   """Get password from user showing asterisks while typing."""


   password = ""


   sys.stdout.write(prompt)


   sys.stdout.flush()


  


   while True:


       char = input()


       if char == "":  # Enter pressed


           break


       password += char


       sys.stdout.write("\033[F")  # Move cursor up one line


       sys.stdout.write(prompt + "*" * len(char))  # Rewrite with asterisks


       sys.stdout.write("\n")  # Move to next line


       sys.stdout.flush()


  


   return password


import sys


from typing import List, Tuple, Dict, Any, Optional


import platform


def get_password_with_asterisks(prompt="Password: "):


   """Get password from user showing asterisks while typing."""


   password = ""


   print(prompt, end='', flush=True)


   if platform.system() == 'Windows':


       import msvcrt


       while True:


           char = msvcrt.getch()


           char = char.decode('utf-8') if isinstance(char, bytes) else char


           if char == '\r' or char == '\n':  # Enter key


               print()


               break


           elif char == '\b':  # Backspace


               if password:


                   password = password[:-1]


                   print('\b \b', end='', flush=True)


           elif char.isprintable():


               password += char


               print('*', end='', flush=True)


   else:  # Unix-like


       import termios


       import tty


       fd = sys.stdin.fileno()


       old_settings = termios.tcgetattr(fd)


       try:


           tty.setraw(fd)


           while True:


               char = sys.stdin.read(1)


               if char == '\r' or char == '\n':  # Enter key


                   print()


                   break


               elif char == '\x7f':  # Backspace


                   if password:


                       password = password[:-1]


                       print('\b \b', end='', flush=True)


               elif char.isprintable():


                   password += char


                   print('*', end='', flush=True)


       finally:


           termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


  


   return password


# GLOBAL CONSTANTS


SHIFT_VAL = 7


PLAYERS_FILE = "players.txt"


HIGHSCORES_FILE = "highscores.txt"


COLORS = ["R", "G", "B", "Y", "W", "O"]


CODE_LENGTH = 4


MAX_ATTEMPTS = 10


# --- HELPER FUNCTIONS ---


def generate_random_username(length: int = 6) -> str:


   """


   Generates a random username consisting of 3 lowercase letters and 3 digits.


   """


   letters = ''.join(random.choices(string.ascii_lowercase, k=3))


   numbers = ''.join(random.choices(string.digits, k=3))


   return letters + numbers


def caesar_encrypt(password: str, shift: int = SHIFT_VAL) -> str:


   """


   Implements a Caesar cipher for letters (A-Z, a-z) and digits (0-9).


   """


   enc = []


   for ch in password:


       if ch.isalpha():


           base = ord("A") if ch.isupper() else ord("a")


           rotated = chr((ord(ch) - base + shift) % 26 + base)


           enc.append(rotated)


       elif ch.isdigit():


           rotated = chr((ord(ch) - ord("0") + shift) % 10 + ord("0"))


           enc.append(rotated)


       else:


           enc.append(ch)


   return "".join(enc)


def check_username_exists(username: str) -> bool:


   """


   Checks if a username exists in the players file.


   """


   try:


       with open(PLAYERS_FILE, "r", encoding="utf-8") as f:


           for line in f:


               line = line.strip()


               if not line:


                   continue


               try:


                   user, _ = line.split(",", 1)


               except ValueError:


                   continue


               if user == username:


                   return True


       return False


   except FileNotFoundError:


       return False


   except IOError:


       return False


# --- NEW/MODIFIED ACCOUNT MANAGEMENT FUNCTIONS ---


def update_password_in_file(username: str, new_enc_pw: str) -> bool:


   """


   Updates the encrypted password for a specific user in the players file.


   Reads all lines, modifies the target line, and rewrites the entire file.


   """


   lines = []


   updated = False


   try:


       with open(PLAYERS_FILE, "r", encoding="utf-8") as f:


           for line in f:


               line = line.strip()


               if not line:


                   lines.append("")


                   continue


               parts = line.split(",", 1)


               if len(parts) == 2 and parts[0] == username:


                   lines.append(f"{username},{new_enc_pw}")


                   updated = True


               else:


                   lines.append(line)


       if updated:


           with open(PLAYERS_FILE, "w", encoding="utf-8") as f:


               f.write('\n'.join(lines) + '\n')


           return True


       return False  # User not found


   except IOError as e:


       print(f"Error reading/writing database: {e}")


       return False


def forgot_password() -> None:


   """


   Handles the password reset process.


   """


   print("\n=== Forgot Password (Password Reset) ===")


   username = input("Enter your username: ").strip().lower()


   if not check_username_exists(username):


       print(f"User '{username}' not found.")


       return


   # Simplified identification step: just confirming the username


   print(f"User '{username}' found. You can now reset your password.")


   while True:


       try:


           # Password input shows asterisks while typing


           new_pw = get_password_with_asterisks("Enter your NEW password: ")


       except (KeyboardInterrupt, EOFError):


           print("\nPassword reset cancelled.")


           return


       if new_pw == "":


           print("Password cannot be empty.")


           continue


       enc_pw = caesar_encrypt(new_pw)


       if update_password_in_file(username, enc_pw):


           print("✅ Password successfully updated!")


           return


       else:


           print("❌ Error updating password. Please try again.")


           return


def register_user() -> None:


   """


   Handles user registration. Password input is VISIBLE.


   """


   print("\n=== User Registration ===")


   random_user = generate_random_username()


   print(f"Suggestion: Use '{random_user}'")


   while True:


       username = input("Enter your username: ").strip().lower()


       if username == "":


           print("Username cannot be empty.")


           continue


       if check_username_exists(username):


           print("Username already taken.")


           continue


       try:


           # Password input shows asterisks while typing


           pw = get_password_with_asterisks("Enter your password: ")


       except (KeyboardInterrupt, EOFError):


           print("\nRegistration cancelled.")


           return


       if pw == "":


           print("Password cannot be empty.")


           continue


       enc_pw = caesar_encrypt(pw)


       try:


           os.makedirs(os.path.dirname(PLAYERS_FILE) or ".", exist_ok=True)


           with open(PLAYERS_FILE, "a", encoding="utf-8") as f:


               f.write(f"{username},{enc_pw}\n")


           print("Registration successful.")


           return


       except IOError as e:


           print(f"Error writing to database: {e}")


           return


def login_user() -> Tuple[bool, str]:


   """


   Handles user login and password verification. Password input is VISIBLE.


   """


   print("\n=== User Login ===")


   while True:


       try:


           username = input("Username: ").strip().lower()


       except (KeyboardInterrupt, EOFError):


           print("\nLogin cancelled.")


           return False, ""


       try:


           # Password input shows asterisks while typing


           pw = get_password_with_asterisks("Password: ")


       except (KeyboardInterrupt, EOFError):


           print("\nLogin cancelled.")


           return False, ""


       user_found = False


       login_successful = False


       try:


           with open(PLAYERS_FILE, "r", encoding="utf-8") as f:


               for line in f:


                   line = line.strip()


                   if not line:


                       continue


                   try:


                       user, stored_enc_pw = line.split(",", 1)


                   except ValueError:


                       continue


                   if user == username:


                       user_found = True


                       if caesar_encrypt(pw) == stored_enc_pw:


                           print("Login successful.")


                           login_successful = True


                       else:


                           print("Access Denied")


                       break


       except FileNotFoundError:


           print("Database file not found. Please register first.")


           return False, ""


       except IOError as e:


           print(f"Error reading database: {e}")


           return False, ""


       if login_successful:


           return True, username


       if not user_found:


           try_again = input(


               "Username not found. Do you want to try again? (Y/N): ").strip().upper()


           if try_again != "Y":


               return False, ""


       else:


           # user found but wrong password


           try_again = input("Try again? (Y/N): ").strip().upper()


           if try_again != "Y":


               return False, ""


# --- GAME LOGIC (Unchanged) ---


def generate_secret_code() -> List[str]:


   secret_code = []


   for i in range(1, CODE_LENGTH+1):


       secret_code.append(random.choice(COLORS))


   return secret_code


def parse_guess(raw: str) -> Optional[List[str]]:


   raw = raw.strip().upper()


   if not raw:


       return None


   for sep in [",", " "]:


       if sep in raw:


           parts = [p for p in (raw.replace(",", " ").split()) if p]


           if len(parts) != CODE_LENGTH:


               return None


           parts = [p[0] for p in parts]


           if all(p in COLORS for p in parts):


               return parts


           return None


   if len(raw) == CODE_LENGTH and all(ch in COLORS for ch in raw):


       return list(raw)


   return None


def score_guess(secret: List[str], guess: List[str]) -> Tuple[int, int]:


   black = sum(1 for s, g in zip(secret, guess) if s == g)


   secret_counts = {}


   guess_counts = {}


   for i in range(len(secret)):


       if secret[i] != guess[i]:


           secret_counts[secret[i]] = secret_counts.get(secret[i], 0) + 1


           guess_counts[guess[i]] = guess_counts.get(guess[i], 0) + 1


   white = 0


   for color, cnt in guess_counts.items():


       white += min(cnt, secret_counts.get(color, 0))


   return black, white


def play_game(username: str) -> Tuple[int, bool]:


   secret = generate_secret_code()


   print("\n=== Mastermind: Guess the 4-color code ===")


   print(


       f"Colors: {', '.join(COLORS)} (use letters). Code length: {CODE_LENGTH}.")


   print(f"You have {MAX_ATTEMPTS} attempts. Repeats allowed.")


   attempts_used = 0


   for attempt in range(1, MAX_ATTEMPTS + 1):


       attempts_used = attempt


       while True:


           raw = input(


               f"Attempt {attempt}/{MAX_ATTEMPTS} - Enter your guess: ")


           guess = parse_guess(raw)


           if guess is None:


               print(


                   f"Invalid guess. Enter {CODE_LENGTH} colors using letters from {COLORS}.")


               continue


           break


       black, white = score_guess(secret, guess)


       print(


           f"Feedback -> Black pegs (correct color+pos): {black}, White pegs (correct color wrong pos): {white}")


       if black == CODE_LENGTH:


           print("You Win! 🎉")


           return attempts_used, True


   print("Game Over! Code was: " + "".join(secret))


   return attempts_used, False


# --- LEADERBOARD LOGIC (Unchanged) ---


def load_highscores() -> Dict[str, int]:


   scores = {}


   try:


       with open(HIGHSCORES_FILE, "r", encoding="utf-8") as f:


           for line in f:


               line = line.strip()


               if not line:


                   continue


               try:


                   user, s = line.split(",", 1)


                   scores[user] = int(s)


               except ValueError:


                   continue


   except FileNotFoundError:


       pass


   except IOError:


       pass


   return scores


def save_highscores(scores: Dict[str, int]) -> None:


   try:


       with open(HIGHSCORES_FILE, "w", encoding="utf-8") as f:


           for user, s in scores.items():


               f.write(f"{user},{s}\n")


   except IOError as e:


       print(f"Error writing highscores: {e}")


def update_leaderboard(username: str, score: int) -> None:


   scores = load_highscores()


   prev = scores.get(username)


   if prev is None or score < prev:


       scores[username] = score


       save_highscores(scores)


       if prev is None:


           print(f"New highscore added for {username}: {score}")


       else:


           print(f"Highscore improved for {username}: {prev} -> {score}")


   else:


       print(


           f"No leaderboard update: {username}'s best is {prev}, your score was {score}")


def display_top5() -> None:


   scores = load_highscores()


   if not scores:


       print("No highscores yet.")


       return


   sorted_scores = sorted(scores.items(), key=lambda kv: (kv[1], kv[0]))


   print("\n=== Top 5 Players ===")


   for i, (user, s) in enumerate(sorted_scores[:5], start=1):


       print(f"{i}. {user} - {s}")


   print("=====================")


# --- MAIN MENU (Modified) ---


def main_menu() -> None:


   """


   Displays the main menu and handles user choices.


   """


   while True:


       print("\nMain Menu")


       print("[R] Register")


       print("[L] Login & Play")


       print("[F] Forgot Password")  # <-- NEW OPTION


       print("[E] Exit")


       choice = input("Your choice: ").strip().upper()


       if choice == "R":


           register_user()


       elif choice == "L":


           success, username = login_user()


           if success:


               attempts, won = play_game(username)


               score = attempts


               update_leaderboard(username, score)


               display_top5()


       elif choice == "F":  # <-- NEW HANDLER


           forgot_password()


       elif choice == "E":


           print("Exiting application. Goodbye! 👋")


           break


       else:


           print("Invalid choice. Please enter R, L, F, or E.")


if __name__ == "__main__":


   try:


       main_menu()


   except KeyboardInterrupt:


       print("\nInterrupted. Goodbye! 👋")


       sys.exit(0)







