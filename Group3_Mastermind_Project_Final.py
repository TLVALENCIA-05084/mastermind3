import random
import string
import os
import sys
from typing import List, Tuple, Dict, Optional
from datetime import datetime # Added import for date/time

# GLOBAL VARIABLE CONSTANTS
SHIFT_VAL = 7
PLAYERS_FILE = "players.txt"
HIGHSCORES_FILE = "highscores.txt"
GAME_HISTORY_FILE = "game_history.txt" # New constant
COLORS = ["R", "G", "B", "Y", "W", "O"]
CODE_LENGTH = 4
MAX_ATTEMPTS = 10


# --- Get Password in file with * (Asterisks) Function (Feature) ---

def get_password_with_asterisks(prompt="Password: "):
    """Get password from user showing asterisks while typing."""
    password = ""
    print(prompt, end="", flush=True)

    if sys.platform != 'win32':
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char == "\r" or char == "\n":  # Enter key
                    print()  # Move to next line
                    break
                elif char == "\x7f" or char == "\x08":  # Backspace
                    if password:
                        password = password[:-1]
                        print("\b \b", end="", flush=True)
                elif char.isprintable():
                    password += char
                    print("*", end="", flush=True)
                elif char == "\x03":  # Ctrl+C
                    raise KeyboardInterrupt
        finally:
            # Restore terminal settings before returning
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    else:
        import msvcrt
        while True:
            char = msvcrt.getch()
            char = char.decode('utf-8') if isinstance(char, bytes) else char
            if char == "\r":  # Enter key
                print()
                break
            elif char == "\b":  # Backspace
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            elif char.isprintable():
                password += char
                print("*", end="", flush=True)
            elif char == "\x03":  # Ctrl+C
                raise KeyboardInterrupt
    return password


# --- Generate Random Username Function ---

def generate_random_username() -> str:
    """Generates a random username consisting of 3 lowercase letters and 3 digits."""
    letters = ''.join(random.choices(string.ascii_lowercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=3))
    return letters + numbers


# --- Caesar Encryption in password in file Function ---

def caesar_encrypt(password: str, shift: int = SHIFT_VAL) -> str:
    """Implements a Caesar cipher for letters (A-Z, a-z) and digits (0-9)."""
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


# --- Check Username in file Function ---

def check_username_exists(username: str) -> bool:
    """Checks if a username exists in the players file."""
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


# --- Update Password in file Function ---

def update_password_in_file(username: str, new_enc_pw: str) -> bool:
    """Updates the encrypted password for a specific user in the players file."""
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
        return False
    except IOError as e:
        print(f"Error reading/writing database: {e}")
        return False


# --- Forgot Password Function (Feature) ---

def forgot_password() -> None:
    """Handles the password reset process."""
    print("\n=== Forgot Password (Password Reset) ===")
    username = input("Enter your username: ").strip().lower()
    if not check_username_exists(username):
        print(f"User '{username}' not found.")
        return

    print(f"User '{username}' found. You can now reset your password.")
    while True:
        try:
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


# --- User Registration & User Login (Main) System Functions ---

def register_user() -> None:
    """Handles user registration."""
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
    """Handles user login and password verification."""
    print("\n=== User Login ===")
    attempts = 0
    MAX_LOGIN_ATTEMPTS = 5
    current_username = ""


    while attempts < MAX_LOGIN_ATTEMPTS:
        if not current_username:
            try:
                username = input("Username: ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print("\nLogin cancelled.")
                return False, ""
            current_username = username


        try:
            pw = get_password_with_asterisks("Password: ")
        except (KeyboardInterrupt, EOFError):
            print("\nLogin cancelled.")
            return False, ""


        attempts += 1  # Increment attempt counter after password entry
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


                    if user == current_username:
                        user_found = True
                        if caesar_encrypt(pw) == stored_enc_pw:
                            print("Login successful.")
                            return True, current_username
                        else:
                            remaining_attempts = MAX_LOGIN_ATTEMPTS - attempts
                            if remaining_attempts > 0:
                                print(
                                    f"Access Denied - {remaining_attempts} attempts remaining")
                            else:
                                print("Maximum login attempts reached.")
                                print("Redirecting to password reset...")
                                forgot_password()
                                return False, ""
                        break


        except FileNotFoundError:
            print("Database file not found. Please register first.")
            return False, ""
        except IOError as e:
            print(f"Error reading database: {e}")
            return False, ""


        if not user_found:
            try_again = input(
                "Username not found. Do you want to try again? (Y/N): ").strip().upper()
            if try_again != "Y":
                return False, ""
            current_username = ""  # Reset username to allow trying a different one
            attempts = 0  # Reset attempts for new username
        elif attempts < MAX_LOGIN_ATTEMPTS:
            try_again = input("Try again? (Y/N): ").strip().upper()
            if try_again != "Y":
                return False, ""


    # If we get here, maximum attempts were reached
    print("Maximum login attempts reached.")
    print("Redirecting to password reset...")
    forgot_password()
    return False, ""


# --- Core Game System Functions ---

def generate_secret_code() -> List[str]:
    return random.choices(COLORS, k=CODE_LENGTH)


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

    white = sum(min(guess_counts.get(color, 0), count)
        for color, count in secret_counts.items())
    return black, white


def guess_position(secret: List[str], guess: List[str]):
    guess_colors = []
    for i in range(len(secret)):
        if secret[i] == guess[i]:
            guess_colors.append("B")
        elif (guess[i] in secret) and (secret[i] != guess[i]):
            guess_colors.append("W")
        else:
            guess_colors.append("X")
    return guess_colors


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
            raw = input(f"Attempt {attempt}/{MAX_ATTEMPTS} - Enter your guess: ")
            guess = parse_guess(raw)
            if guess is None:
                print(
                    f"Invalid guess. Enter {CODE_LENGTH} colors using letters from {COLORS}.")
                continue
            break

        black, white = score_guess(secret, guess)
        guess_colors = guess_position(secret, guess)
        print(f"Feedback -> Black pegs (correct color+position): {black}, White pegs (correct color/wrong position): {white}")
        print(f"Color Arrangement: {guess_colors}")

        if black == CODE_LENGTH:
            print("You Win! 🎉")
            return attempts_used, True

    print("Game Over! Code was: " + "".join(secret))
    return attempts_used, False


# --- Player Game History Management Functions ---

def load_game_history() -> List[Tuple[str, str, int]]:
    """Loads game history from the file: (Date, Username, Score)"""
    history = []
    try:
        with open(GAME_HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    date, user, score = line.split(",", 2)
                    history.append((date, user, int(score)))
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    except IOError:
        pass
    return history


def save_game_result(username: str, score: int) -> None:
    """Appends a new game result to the history file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp},{username},{score}\n"
    try:
        os.makedirs(os.path.dirname(GAME_HISTORY_FILE) or ".", exist_ok=True)
        with open(GAME_HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except IOError as e:
        print(f"Error writing game history: {e}")


def display_game_history() -> None:
    """Displays the entire game history sorted by date (most recent first)."""
    history = load_game_history()
    if not history:
        print("\nNo game history recorded yet.")
        return

    # Sort history by date (first element in the tuple) in descending order
    sorted_history = sorted(history, key=lambda x: x[0], reverse=True)

    print("\n📜 === Game History (Most Recent First) ===")
    print(f"{'Date':<19} | {'Username':<15} | {'Attempts':<8}")
    print("-" * 46)
    for date, user, score in sorted_history:
        # Display the date part only for a cleaner look
        display_date = date.split(' ')[0]
        print(f"{display_date:<19} | {user:<15} | {score:<8}")
    print("=" * 46)


# --- Leaderboard Functions ---

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

    # Sort by score (ascending) then by username (alphabetical)
    sorted_scores = sorted(scores.items(), key=lambda kv: (kv[1], kv[0]))
    print("\n🏆 === Top 5 Leaderboard (Fewer Attempts is Better) ===")
    for i, (user, s) in enumerate(sorted_scores[:5], start=1):
        print(f"{i}. {user} - {s} attempts")
    print("=======================================================")


# --- Main Menu Function ---

def main_menu() -> None:
    """Displays the main menu and handles user choices."""
    while True:
        print("\nMain Menu")
        print("[R] Register")
        print("[L] Login & Play")
        print("[F] Forgot Password")
        print("[E] Exit")
        choice = input("Your choice: ").strip().upper()

        if choice == "R":
            register_user()
        elif choice == "L":
            success, username = login_user()
            if success:
                attempts, won = play_game(username)
                # Game completed, always save the result
                save_game_result(username, attempts)
               
                # Only update leaderboard if the game was won
                if won:
                    update_leaderboard(username, attempts)
               
                # Display leaderboard and history automatically after any game
                display_top5()
                display_game_history()
        elif choice == "F":
            forgot_password()
        elif choice == "E":
            print("Exiting application. Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter R, L, F, or E.")


# --- Call-Out the Main Menu Function ---

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye! 👋")
        sys.exit(0)
