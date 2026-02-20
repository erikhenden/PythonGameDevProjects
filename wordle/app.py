import requests


def main():
    # Welcome message
    print(welcome_message())

    # Settings
    difficulty = get_int("Enter difficulty (a number between 1-5 where 1 = easy and 5 = hard): ")
    word_length = get_int("Enter word length (3-12): ")
    print(f"You set a difficulty of {difficulty} and a word length of {word_length}.")

    # Get a random word
    word = get_response(f"https://random-word-api.herokuapp.com/word?length={word_length}&diff={difficulty}")
    print(word)



def welcome_message():
    return "Welcome to the Wordle Game!"


def get_str(prompt):
    while True:
        try:
            return input(prompt).strip().lower()
        except ValueError:
            print("Invalid input, please try again.")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input, please try again.")


def get_response(url):
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Request Exception: {e}"


if __name__ == "__main__":
    main()
