import random
import string
import os
import sys
import platform

# GLOBAL CONSTANTS
SHIFT_VAL = 7
PLAYERS_FILE = "players.txt"
HIGHSCORES_FILE = "highscores.txt"
COLORS = ["R", "G", "B", "Y", "W", "O"]
CODE_LENGTH = 4
MAX_ATTEMPTS = 10


def get_password_with_asterisks(prompt="Password: "):
    """Get password from user showing asterisks while typing."""
    password = ""
    print(prompt, end='', flush=True)
    if platform.system() == 'Windows':
        import msvcrt
        while True:
            char = msvcrt.getch().decode('utf-8')
            if char in ['\r', '\n']:
                print()
                break
            elif char == '\b' and password:
                password = password[:-1]
                print('\b \b', end='', flush=True)
            elif char.isprintable():
                password += char
                print('*', end='', flush=True)
    else:  # Unix-like
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
                elif char == '\x7f' and password:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
                elif char.isprintable():
                    password += char
                    print('*', end='', flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return password


def generate_random_username(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=3)) + ''.join(random.choices(string.digits, k=3))


def caesar_encrypt(password: str, shift: int = SHIFT_VAL) -> str:
    result = []
    for ch in password:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        elif ch.isdigit():
            result.append(chr((ord(ch) - ord("0") + shift) % 10 + ord("0")))
        else:
            result.append(ch)
    return "".join(result)


def check_username_exists(username: str) -> bool:
    try:
        with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
            return any(line.strip().split(",", 1)[0] == username for line in f if "," in line)
    except (FileNotFoundError, IOError):
        return False


def update_password_in_file(username: str, new_enc_pw: str) -> bool:
    try:
        with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        for i, line in enumerate(lines):
            parts = line.split(",", 1)
            if len(parts) == 2 and parts[0] == username:
                lines[i] = f"{username},{new_enc_pw}"
                break
        else:
            return False
        with open(PLAYERS_FILE, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines) + '\n')
        return True
    except IOError as e:
        print(f"Error updating password: {e}")
        return False


def forgot_password():
    print("\n=== Forgot Password ===")
    username = input("Enter your username: ").strip().lower()
    if not check_username_exists(username):
        print(f"User '{username}' not found.")
        return
    new_pw = get_password_with_asterisks("Enter your NEW password: ")
    if not new_pw:
        print("Password cannot be empty.")
        return
    if update_password_in_file(username, caesar_encrypt(new_pw)):
        print("✅ Password successfully updated!")
    else:
        print("❌ Error updating password.")


def register_user():
    print("\n=== User Registration ===")
    print(f"Suggestion: Use '{generate_random_username()}'")
    while True:
        username = input("Enter your username: ").strip().lower()
        if not username:
            print("Username cannot be empty.")
            continue
        if check_username_exists(username):
            print("Username already taken.")
            continue
        pw = get_password_with_asterisks("Enter your password: ")
        if not pw:
            print("Password cannot be empty.")
            continue
        try:
            with open(PLAYERS_FILE, "a", encoding="utf-8") as f:
                f.write(f"{username},{caesar_encrypt(pw)}\n")
            print("Registration successful.")
            return
        except IOError as e:
            print(f"Error writing to database: {e}")
            return


def login_user() -> tuple[bool, str]:
    print("\n=== User Login ===")
    username = input("Username: ").strip().lower()
    pw = get_password_with_asterisks("Password: ")
    try:
        with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",", 1)
                if len(parts) == 2 and parts[0] == username:
                    if caesar_encrypt(pw) == parts[1]:
                        print("Login successful.")
                        return True, username
                    else:
                        print("Access Denied.")
                        return False, ""
        print("Username not found.")
    except FileNotFoundError:
        print("Database not found. Please register first.")
    except IOError as e:
        print(f"Error reading database: {e}")
    return False, ""


def generate_secret_code() -> list[str]:
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]


def parse_guess(raw: str) -> list[str] | None:
    raw = raw.strip().upper()
    if not raw:
        return None
    parts = [p for p in raw.replace(",", " ").split() if p]
    if len(parts) == CODE_LENGTH and all(p[0] in COLORS for p in parts):
        return [p[0] for p in parts]
    return None


def score_guess(secret: list[str], guess: list[str]) -> tuple[int, int]:
    black = sum(s == g for s, g in zip(secret, guess))
    secret_counts, guess_counts = {}, {}
    for s, g in zip(secret, guess):
        if s != g:
            secret_counts[s] = secret_counts.get(s, 0) + 1
            guess_counts[g] = guess_counts.get(g, 0) + 1
    white = sum(min(secret_counts.get(c, 0), n) for c, n in guess_counts.items())
    return black, white


def play_game(username: str) -> tuple[int, bool]:
    secret = generate_secret_code()
    print("\n=== Mastermind ===")
    print(f"Colors: {', '.join(COLORS)}. Code length: {CODE_LENGTH}. Attempts: {MAX_ATTEMPTS}.")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        while True:
            guess = parse_guess(input(f"Attempt {attempt}/{MAX_ATTEMPTS}: "))
            if guess:
                break
            print("Invalid guess.")
        black, white = score_guess(secret, guess)
        print(f"Feedback -> Black: {black}, White: {white}")
        if black == CODE_LENGTH:
            print("🎉 You Win! 🎉")
            return attempt, True
    print("Game Over! The correct code was:", "".join(secret))
    return MAX_ATTEMPTS, False


def load_highscores() -> dict[str, int]:
    try:
        with open(HIGHSCORES_FILE, "r", encoding="utf-8") as f:
            return {u: int(s) for u, s in (line.strip().split(",", 1) for line in f if line.strip())}
    except (FileNotFoundError, IOError, ValueError):
        return {}


def save_highscores(scores: dict[str, int]) -> None:
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
        print(f"🏆 Highscore updated for {username}: {prev or 'N/A'} → {score}")
    else:
        print(f"No update. Best: {prev}, This: {score}")


def display_top5() -> None:
    scores = load_highscores()
    if not scores:
        print("No highscores yet.")
        return
    sorted_scores = sorted(scores.items(), key=lambda kv: (kv[1], kv[0]))
    print("\n=== Top 5 Players ===")
    for i, (user, s) in enumerate(sorted_scores[:5], start=1):
        print(f"{i}. {user} - {s}")


def print_welcome_note():
    print("=" * 50)
    print("WELCOME TO THE MASTERMIND GAME")
    print("Submitted by: Tristan, Ben, Nikko, JB, Fherlyn, Shannen, Brainard")
    print("CMSC 202 - Group 3")
    print("Submitted to: Ms. Kat. Abriol")
    print("=" * 50)
    print(" GAME MECHANICS:")
    print("1️ The computer randomly generates a 4-color code.")
    print("2️ You must guess the code using colors: R, G, B, Y, W, O.")
    print("3️ After each guess, you'll get feedback:")
    print("   - Black: Correct color in the correct position.")
    print("   - White: Correct color but in the wrong position.")
    print(f"4️ You have {MAX_ATTEMPTS} attempts to guess the correct code.")
    print("5️ Beat your best score and climb the leaderboard!")
    print("=" * 50)


def main_menu() -> None:
    while True:
        print("\nMain Menu\n[R] Register\n[L] Login & Play\n[F] Forgot Password\n[E] Exit")
        choice = input("Your choice: ").strip().upper()
        if choice == "R":
            register_user()
        elif choice == "L":
            success, username = login_user()
            if success:
                attempts, _ = play_game(username)
                update_leaderboard(username, attempts)
                display_top5()
        elif choice == "F":
            forgot_password()
        elif choice == "E":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        print_welcome_note()
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye! 👋")
        sys.exit(0)
