# logout.py

def logout():
    try:
        # Clear the session (remove logged-in user)
        with open("session.txt", "w") as session_file:
            session_file.write("")
        print("\n✅ You have been successfully logged out.\n")
    except FileNotFoundError:
        print("\n⚠️ No session found. You are not logged in.\n")
