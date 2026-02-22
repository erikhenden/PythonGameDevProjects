guesses = [
    ("s", "correct"),
    ("a", "correct"),
    ("b", "incorrect"),
    ("c", "incorrect"),
    ("s", "incorrect"),
]

used_letters = {char: status for char, status in guesses}

print(used_letters)
print(guesses)