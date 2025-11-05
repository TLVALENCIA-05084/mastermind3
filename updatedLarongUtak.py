import os
import sys
import random
import string
import platform
from typing import List, Tuple, Dict, Optional

def get_password_with_asterisks(prompt="Password: "):
    """Get password from user showing asterisks while typing."""
    password = ""
    print(prompt, end='', flush=True)

    if platform.system() == 'Windows':
        import msvcrt
        while True:
            char = msvcrt.getch()
            char = char.decode('utf-8') if isinstance(char, bytes) else char
            if char in ['\r', '\n']:
                print()
                break
            elif char == '\b':
                if password:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            elif char.isprintable():
                password += char
                print('*', end='', flush=True)
    else:
        import termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char in ['\r', '\n']:
                    print()
                    break
                elif char == '\x7f':
                    if password:
                        password = password[:-1]
                        print('\b \b', end='', flush=True)
                elif char.isprintable():
                    password += char
                    print('*', end='', flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return password

# --- GLOBAL CONSTANTS ---
SHIFT_VAL = 7
PLAYERS_FILE = "players.txt"
HIGHSCORES_FILE = "highscores.txt"
COLORS = ["R", "G", "B", "Y", "W", "O"]
CODE_LENGTH = 4
MAX_ATTEMPTS = 10

# --- HELPER FUNCTIONS ---
def generate_random_username(length: int = 6) -> str:
    letters = ''.join(random.choices(string.ascii_lowercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=3))
    return letters + numbers

def caesar_encrypt(password: str, shift: int = SHIFT_VAL) -> str:
    enc = []
    for ch in password:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            enc.append(chr((ord(ch) - base + shift) % 26 + base))
        elif ch.isdigit():
            enc.append(chr((ord(ch) - ord("0") + shift) % 10 + ord("0")))
        else:
            enc.append(ch)
    return "".join(enc)

def check_username_exists(username: str) -> bool:
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
    except (FileNotFoundError, IOError):
        return False

# --- ACCOUNT MANAGEMENT ---
def update_password_in_file(username: str, new_enc_pw: str) -> bool:
    lines, updated = [], False
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

def forgot_password() -> None:
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

def register_user() -> None:
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
    print("\n=== User Login ===")
    while True:
        try:
            username = input("Username: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nLogin cancelled.")
            return False, ""
        try:
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
            if input("Username not found. Try again? (Y/N): ").strip().upper() != "Y":
                return False, ""
        else:
            if input("Wrong password. Try again? (Y/N): ").strip().upper() != "Y":
                return False, ""

# --- GAME LOGIC ---
def generate_secret_code() -> List[str]:
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]

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
            return parts if all(p in COLORS for p in parts) else None
    return list(raw) if len(raw) == CODE_LENGTH and all(ch in COLORS for ch in raw) else None

def score_guess(secret: List[str], guess: List[str]) -> Tuple[int, int]:
    black = sum(1 for s, g in zip(secret, guess) if s == g)
    secret_counts, guess_counts = {}, {}
    for i in range(len(secret)):
        if secret[i] != guess[i]:
            secret_counts[secret[i]] = secret_counts.get(secret[i], 0) + 1
            guess_counts[guess[i]] = guess_counts.get(guess[i], 0) + 1
    white = sum(min(cnt, secret_counts.get(color, 0)) for color, cnt in guess_counts.items())
    return black, white

def play_game(username: str) -> Tuple[int, bool]:
    secret = generate_secret_code()
    print("\n=== Mastermind: Guess the 4-color code ===")
    print(f"Colors: {', '.join(COLORS)} (use letters). Code length: {CODE_LENGTH}.")
    print(f"You have {MAX_ATTEMPTS} attempts. Repeats allowed.")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        while True:
            raw = input(f"Attempt {attempt}/{MAX_ATTEMPTS} - Enter your guess: ")
            guess = parse_guess(raw)
            if guess is None:
                print(f"Invalid guess. Enter {CODE_LENGTH} colors using letters from {COLORS}.")
                continue
            break
        black, white = score_guess(secret, guess)
        print(f"Feedback -> Black pegs: {black}, White pegs: {white}")
        if black == CODE_LENGTH:
            print("You Win! 🎉")
            return attempt, True
    print("Game Over! Code was: " + "".join(secret))
    return MAX_ATTEMPTS, False

# --- LEADERBOARD ---
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
    except (FileNotFoundError, IOError):
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
        msg = f"New highscore for {username}: {score}" if prev is None else f"Highscore improved: {prev} -> {score}"
        print(msg)
    else:
        print(f"No update: {username}'s best is {prev}, your score was {score}")

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

# --- MAIN MENU ---
def main_menu() -> None:
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
                update_leaderboard(username, attempts)
                display_top5()
        elif choice == "F":
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
