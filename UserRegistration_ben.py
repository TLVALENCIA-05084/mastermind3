import sys
import termios
import tty
import re

shift_val = 7

# Function to 'encrypt' a password using Caesar's Cipher
def caesar_encrypt(password, shift=shift_val):
    enc_pw = ''
    for char in password:
        if char.isalpha():
            base_char = ord('A') if char.isupper() else ord('a')
            enc_pw += chr((ord(char) - base_char + shift) % 26 + base_char)
        elif char.isdigit():
            enc_pw += chr((ord(char) - ord('0') + shift) % 10 + ord('0'))
        else:
            enc_pw += char
    return enc_pw


# Function to show * while typing password
def input_password(prompt="Password: "):
    print(prompt, end="", flush=True)
    password = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch in ["\r", "\n"]:
                print()
                break
            elif ch == "\x7f":  # backspace
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                password += ch
                sys.stdout.write("*")
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return password


# Function to validate password strength
def validate_password(password):
    if len(password) > 10:
        print("❌ Password too long. Maximum length is 10 characters.")
        return False
    if not re.search(r"[A-Z]", password):
        print("❌ Password must contain at least one uppercase letter.")
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        print("❌ Password must contain at least one special character.")
        return False
    return True


# === USER REGISTRATION ===
def register_user():
    print("\n=== USER REGISTRATION ===")
    username = input("Create a username: ").strip().lower()

    # Check if username already exists
    try:
        with open("players.txt", "r", encoding="utf-8") as players:
            for line in players:
                existing_user, _ = line.strip().split(",")
                if existing_user == username:
                    print("❌ Username already exists. Please choose another one.")
                    return
    except FileNotFoundError:
        pass

    # Show password requirements before input
    print("\n🔑 Password Requirements:")
    print("- Maximum of 10 characters")
    print("- Must include at least 1 uppercase letter")
    print("- Must include at least 1 special character (e.g. !, @, #, $, %)\n")

    # Input password
    while True:
        password = input_password("Create a password: ")
        if not validate_password(password):
            continue
        confirm_pw = input_password("Confirm password: ")
        if password != confirm_pw:
            print("❌ Passwords do not match. Please try again.")
            continue
        break

    encrypted_pw = caesar_encrypt(password)

    # Save to file
    with open("players.txt", "a", encoding="utf-8") as players:
        players.write(f"{username},{encrypted_pw}\n")

    print(f"\n✅ Registration successful! You can now log in as '{username}'.")
    


if __name__ == "__main__":
    register_user()





