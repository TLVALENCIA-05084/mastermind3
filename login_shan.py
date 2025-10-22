from getpass import getpass

shift_val = 7

#Function to 'encrypt' a password using Caesar's Cipher
def caesar_encrypt(password, shift=shift_val):
    enc_pw = ''

    for char in password:
        #Check if the current char is an alphabet
        if char.isalpha():  
            #Set the order of the base character starting from 'A' (returns 65) if it is in uppercase, 'a' (returns 97) if it is in lowercase                                                    
            base_char = ord('A') if char.isupper() else ord('a') 

            #This formula ensures that the encrypted character is within the range of the alphabet with respect to letter case; Store the encrypted password one character per iteration.
            enc_pw += chr((ord(char) - base_char + shift) % 26 + base_char) 

        #Check if the current char is a digit  
        elif char.isdigit():
            #This formula ensures that the encrypted character is within the range of digits                                                   
            enc_pw += chr((ord(char)- ord('0') + shift ) % 10 + ord('0'))     

        else:
            #Special characters are skipped and not encrypted
            enc_pw += char

    return enc_pw

again = True
while again == True:
    #Enter username; input data will then be 'stripped' off white spaces and converted to lowercase for simplicity since this will be case-insensitive.
    input_username = input('Username: ').strip().lower()

    #Enter password using getpass for secrecy
    input_pw = getpass('Password: ')
    #Or use input for a visible password input
    #input_pw = input('Password: ')

    #Open database for player details (username and password).
    with open('players.txt', 'r', encoding='utf=8') as players:
        #Check every line in the opened players.txt file
        for line in players:
            user, enc_pw = line.strip().split(',')

            #Check if the user matches with the input_user
            if user == input_username:

                #Check if the enc_pw associated with the user matches to that of the encrypted input_pw of the input_username.
                if caesar_encrypt(input_pw) == enc_pw:
                    #If it matches, then the user is logged in.
                    print(f'Login successful. Welcome back, {user}!')
                    try_again = 'N'
                else:
                    #Otherwise, unsuccessful login and the user is prompted to try again.
                    try_again = input('Incorrect password. Do you want to try again? Y / N ')
                
                #Since the username has been found (or matched), break to stop the loop from reading the next lines in the database regardless of the correctness of the entered password.
                break
            else:
                try_again = input('Username not found. Do you want to try again? Y / N ')

    if try_again == 'N':
        again = False
    else:
        again = True
