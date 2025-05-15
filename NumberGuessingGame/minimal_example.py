import random

random_number = random.randint(0, 100)
attempts = 0
user_guess = None

while user_guess != random_number:  # Continue the game until user_guess equals the correct answer

    # Validate user input
    while True:
        user_guess = input("\nPlease enter your guess (a number between 0 and 100) \n>> ")
        try:
            user_guess = int(user_guess)  # Convert string to integer
            break
        except ValueError:
            print("\nPlease enter a valid number")

    # Check if user_guess is higher or lower than correct answer
    if int(user_guess) < random_number:
        print("\nThe correct number is higher")
    elif int(user_guess) > random_number:
        print("\nThe correct number is lower")

    attempts += 1  # Increase attempt-counter for each loop

print(f"\nCongratulations, you guessed it! The correct number was {random_number}")  # Displayed when while loop is finished