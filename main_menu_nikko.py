# Start the Program

import random

def show_menu_01():
    print()
    print("Welcome to the Mastermind Game!")
    print()
    print("CMSC 202 Project Group 3")
    print()
    print("Members:")
    print("1. Tristan Joseph Valencia; 2. Fherlyn Charl Yet; 3. Ben-Rasheed Salim; 4. Jonas Bareng;")
    print("5. Nikko Paulo Ilar; 6. Brainard Ardona; 7. Shannen Dorothy Martir")
    print()
    print("Faculty-In-Charge: Ma'am Kat M. Abriol-Santos")
    print()

def show_menu_02():
    print()


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


def main_menu():

    while True:

        show_menu_01()
        show_menu_02()

        choice = input("Enter your choice: ")

        if choice == '0':
            break

        if choice in ['1', '2']:
            username = user_username_test("Enter Username: ")
            password = user_password_test("Enter Password: ")

            if choice == '1':
                username = user_username_input(username)
                password = user_password_input(password)
                print(username)
                print(password)
            elif choice == '2':
                print()
        
        else:
            print()
            print("Invalid Input!")
            print()


if __name__ == "__main__":
    main_menu()

# Terminate the Program
