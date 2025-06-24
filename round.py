import random
from boxes import Box
from players import Player

def play_round(player_type):
# Args: player_type (bool): If True, the player will switch boxes; if False, they will keep their initial choice.
    player = Player(player_type)
    print(f"Starting a new round with {player.name} who will {'switch' if player_type else 'keep'} their box")

# Generate 3 boxes.
    boxes = [Box(_) for _ in range(1, 4)]
    winning_box = random.SystemRandom().choice(boxes)
    winning_box.has_car = True

# Player picks a box.
    print(f"Host: I have placed a car in one of these boxes, the other two contain a goat. {player.name}, please choose a box.")
    chosen_box = player.choose_box(boxes)
    chosen_box.is_chosen = True
    print(f"{player.name}: I would like box number {chosen_box.number} please.")

# Host Eliminates a losing box.
    for box in boxes:
        if box.is_chosen == False and box.has_car == False:
            box.is_opened = True
            print(f"Host: I can reveal that box number {box.number} has a {'car' if box.has_car else 'goat'} inside it.")
            boxes.remove(box)
            break

# Player chooses to keep or switch.
    print(f"Host: Now, {player.name}, you have the option to keep your box or switch to the other remaining box.")
    final_choice = player.keep_or_switch(boxes)

# Result of the round
    round_result = final_choice.has_car
    if final_choice == player.first_choice:
        print(f"{player.name}: I have decided to keep my box.")
        if final_choice.has_car:
            print(f"Congratulations {player.name}, you have won a car!")
        else:
            print(f"Sorry {player.name}, you have won the goat.")
        return round_result
    else:
        print(f"{player.name}: I have decided to switch my box!")
        if final_choice.has_car:
            print(f"Congratulations {player.name}, you have won a car!")
        else:
            print(f"Sorry {player.name}, you have won the goat.")
    return round_result