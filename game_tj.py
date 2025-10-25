import random

print("""There are six colors that you can use to guess the secret code.\nRed\nGreen\nBlue\nYellow\nWhite\nOrang\nThere are four colors in the secret code.\nCan you guess them all?""")
colors = ["r","g","b","y","w","o"]

def generate_secret_code(colors):
    secret_code = []
    for i in range(1,5):
        secret_code.append(random.choice(colors))
    return secret_code
def right_guess (colors):
    return None
def right_color_wrong_guess ():
    return None
def wrong_guess ():
    return None
def main_game ():
    return None
