import hashlib
import os

# File to store usernames and passwords
FILE_NAME = "players.txt"

# Helper functions
def encrypt_password(password):
    """Encrypt password using SHA-256 hashing."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from file into a dictionary."""
    users = {}
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            for line in f:
                username, hashed_password = line.strip().split(",")
                users[username] = hashed_password
    return users

def save_user(username, hashed_password):
    """Save new user to file."""
    with open(FILE_NAME, "a") as f:
        f.write(f"{username},{hashed_password}\n")

# --- User Authentication ---
print("Welcome! Register or Login.")

username = input("Enter username: ").strip()
password = input("Enter password: ").strip()

users = load_users()

if username in users:
    # Existing user: verify password
    hashed_input = encrypt_password(password)
    if hashed_input == users[username]:
        print(f"Access Granted. Welcome back, {username}!")
    else:
        print("Access Denied. Wrong password.")
else:
    # New user: register
    hashed_password = encrypt_password(password)
    save_user(username, hashed_password)
    print(f"Registration successful. Welcome, {username}!")



