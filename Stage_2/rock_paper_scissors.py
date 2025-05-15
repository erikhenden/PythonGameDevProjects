import random
import time

round_number = 0
player_score = 0
computer_score = 0
rps_list = ["r", "p", "s"]  # (rock, paper, scissors)
playing_round = False

running = True
while running:
    menu_choice = input("\n'n' = New round \n's' = Score \n'q' = Quit \n>> ")
    if menu_choice == "q":  # Quit game
        print("\nSee you later!")
        running = False

    elif menu_choice == 'n':  # Play a round
        playing_round = True
        while playing_round:

            computer_choice = random.choice(rps_list)

            # Validate user input
            while True:
                player_choice = input("\n'r' = rock, 'p' = paper, 's' = scissors \n'b' = Back to main menu \n>> ")
                if player_choice == 'b':
                    playing_round = False
                    break
                elif player_choice not in rps_list:
                    print("Please enter a valid choice")
                else:
                    break
            if playing_round is False:  # back to main menu
                break

            # Build tension by adding time
            print("Checking winner...")
            time.sleep(1.3)

            # Check winner
            if computer_choice == "r" and player_choice == "p" or computer_choice == "p" and player_choice == "s" or computer_choice == "s" and player_choice == "r":
                player_score += 1
                print("\nPlayer takes the round!")
            elif computer_choice == player_choice:
                print("\nEqual!")
            else:
                computer_score += 1
                print("\nComputer takes the round!")

            # Display current score
            print("\n________ Score ________")
            print(f"Player: {player_score} - Computer: {computer_score}")

            # Increase round count
            round_number += 1

    elif menu_choice == "s":
        print("\n________ Score ________")
        print(f"Player: {player_score} - Computer: {computer_score}")