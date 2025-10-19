# Start the Program

# import random
from show_menu import show_menu_01
from show_menu import show_menu_02
from user_login import user_username_test
from user_login import user_password_test
from user_login import user_username_input
from user_login import user_password_input


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
