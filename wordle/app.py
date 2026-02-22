import requests


class Stats:
    def __init__(self):
        self.stats = []

    def add_stat(self, name, difficulty, word_length, guesses, correct_word):
        self.stats.append({"name": name,
                           "difficulty": difficulty,
                           "word_length": word_length,
                           "guesses": guesses,
                           "correct?": correct_word
                           })

    def display_stats(self):
        for entry in self.stats:
            print(f"{entry['name']}, "
                  f"difficulty: {entry['difficulty']}, "
                  f"word length: {entry['word_length']}, "
                  f"guesses: {entry['guesses']}, "
                  f"correct?: {entry['correct?']}"
                  )


def main():

    # Initialize Stat class
    stats = Stats()

    # Welcome message
    print(welcome_message())

    name = get_str("Enter your name: ")

    # Main menu loop
    running = True
    while running:

        print("""Main Menu:
p. Play
h. Highscores
q. Quit
        """)
        choice = get_str(">> ").strip().lower()

        if choice == "q":  # Quit
            print("Goodbye!")
            running = False

        elif choice == "p":  # Play
            play(name, stats)

        elif choice == "h":
            stats.display_stats()


def welcome_message():
    return "Welcome to the Wordle Game!\n"


def play(player_name, stat_class, rounds=5):

    won = False

    # Get difficulty
    while True:
        difficulty = get_int("Enter difficulty (a number between 1-5 where 1 = easy and 5 = hard): ")
        if difficulty < 1 or difficulty > 5:
            print("Invalid difficulty, please try again.")
        else:
            break

    # Get word length
    while True:
        word_length = get_int("Enter word length (3-12): ")
        if word_length < 3 or word_length > 12:
            print("Invalid word length, please try again.")
        else:
            break

    print(f"You set a difficulty of {difficulty} and a word length of {word_length}.")

    # Create a "hidden word" to mark correct characters
    hidden_word = "-" * word_length

    url_modified = f"https://random-word-api.herokuapp.com/word?length={word_length}&diff={difficulty}"

    # Get a random word
    response = get_response(url_modified)[0]
    if response is None:
        print("Problems/error with the url / requests... Can't get a valid word.")
        return
    word = response[0]

    print("A word has been generated...")

    # Game loop
    for rnd in range(rounds):
        print(f"\nRound: {rnd + 1}")
        guess = get_str("Enter your guess: ")

        # Check guess against word
        for i, char in enumerate(guess):
            if char in word:
                # Check position
                if char == word[i]:
                    hidden_word = hidden_word[:i] + "!" + hidden_word[i + 1:]
                else:
                    hidden_word = hidden_word[:i] + "?" + hidden_word[i + 1:]

        # Display correct and incorrect characters
        print(hidden_word)

        # Check if the guess is correct, or "game over"
        if guess == word:
            print(f"You correctly guessed the word {word}! Congratulations!")
            won = True
            stat_class.add_stat(player_name, difficulty, word_length, rnd+1, won)
            break
        elif guess != word and rnd == rounds - 1:
            stat_class.add_stat(player_name, difficulty, word_length, rnd + 1, won)
            print(f"The word is {word}. Unfortunately, you did not get it right this time...\nBetter luck next time!\n")

        # Reset hidden_word
        hidden_word = "-" * word_length


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
        response = requests.get(url, timeout=5)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None


if __name__ == "__main__":
    main()
