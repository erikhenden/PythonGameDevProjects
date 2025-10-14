"""🕹️ Game Project 2: Quiz Game
Store questions/answers in a dictionary

Randomly select questions

Score tracking with results"""

import random
from capitals import capitals_norsk


def main():
    score = 0
    round_count = 1
    closed = set()

    quizzing = True
    while quizzing:

        # Show round info
        print(f"\n--- Round {round_count}, score: {score} ---")

        # Get question and answer
        question, answer = get_q_and_a(capitals_norsk, closed)
        closed.add(question)

        # Write question
        print(f"What is the capitol of {question}?")

        # Get user input
        user_answer = input("Answer: ").strip().lower()

        # Check answer
        if user_answer == answer:
            print("Correct, the answer is", answer)
            score += 1
        else:
            print("Wrong, the answer is", answer)

        round_count += 1


def get_q_and_a(q, closed):
    while True:
        choice = random.choice(q)
        question, answer = next(iter(choice.items()))
        if question.lower() not in closed:
            return question.lower(), answer.lower()


if __name__ == "__main__":
    main()