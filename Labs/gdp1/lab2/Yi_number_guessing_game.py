import random

secret_number = random.randrange(1, 129)

guess = 0
guesses = []
stop = False
MAX_GUESSES = 7

while guess != secret_number and not stop:
    if (len(guesses) >= MAX_GUESSES):
        print("Maximum Guesses have reach. Exit the Program")
        break

    guess = input("Guess a number 1 to 128: ")
    if (guess == "q"):
        print("You have quit the game")
        stop = True
    elif not(guess.isdigit()):
        print("Please enter a valid integer between 1 and 128")
        continue
    else:
        guess = int(guess)
        guesses.append(guess)
        if guess < secret_number:
            print("Too low.")
        elif guess > secret_number:
            print("Too high.")
        else:
            print("Correct!")

if (not stop):
    print("Your guesses:", " ".join(map(str, guesses)), end=" ")
