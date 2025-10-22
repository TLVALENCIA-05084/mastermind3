def user_username_test(prompt):
    while True:
        try:
            user_num = str(input(prompt))
            if user_num == "1234":
                return user_num
            else:
                print("Invalid Input. for username.")
        except ValueError:
            print("Invalid Input. Please enter correct username.")

def user_password_test(prompt):
    while True:
        try:
            pass_num = str(input(prompt))
            if pass_num == "1234":
                return pass_num
            else:
                print("Invalid Input. for password.")
        except ValueError:
            print("Invalid Input. Please enter correct password.")

def user_username_input(username):
    return username

def user_password_input(password):
    return password
