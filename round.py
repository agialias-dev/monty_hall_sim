import random, sys, getopt
from boxes import Box
from players import Player

def play_round(player_type, verbose):
# Args:
#   player_type (bool): If True, the player will switch boxes; if False, they will keep their initial choice.
#   verbose (bool): if enabled prints enhanced information.
    
#initialization
    if verbose == True:
        def vprint(print_data):
            print(print_data)
    else:
        def vprint(print_data):
            pass
    player = Player(player_type)
    vprint(f"VERBOSE: {repr(player)}")
    print(f"Host: Welcome {player.name}, to Keep OR Switch!")

# Generate 3 boxes.
    boxes = [Box(_) for _ in range(1, 4)]
    winning_box = random.SystemRandom().choice(boxes)
    winning_box.has_car = True
    vprint(f"VERBOSE: {boxes}")

# Player picks a box.
    print(f"Host: I have placed a car in one of these three boxes, the other two contain a goat. {player.name}, please choose a box.")
    chosen_box = player.choose_box(boxes)
    chosen_box.is_chosen = True
    vprint(f"VERBOSE: Chosen box = {repr(chosen_box)}")
    print(f"{player.name}: I would like box number {chosen_box.number} please.")

# Host Eliminates a losing box.
    for box in boxes:
        if box.is_chosen == False and box.has_car == False:
            box.is_opened = True
            print(f"Host: I can reveal that box number {box.number} had a {'car' if box.has_car else 'goat'} inside it, and I will now remove it from the game.")
            vprint(f"VERBOSE: Host removed {repr(box)}")
            boxes.remove(box)
            continue

# Player chooses to keep or switch.
    print(f"Host: Now, {player.name}, you have the option to keep your original box or switch to the remaining box.")
    final_choice = player.keep_or_switch(boxes)

# Result of the round
    round_result = final_choice.has_car
    vprint(f"VERBOSE: Final choice is {repr(final_choice)}")
    if final_choice == player.first_choice:
        print(f"{player.name}: I have decided to keep my box.") 
        if final_choice.has_car:
            print(f"Host: Congratulations {player.name}, you have won a car!")
        else:
            print(f"Host: Sorry {player.name}, you have won the goat.")
        return round_result
    else:
        print(f"{player.name}: I have decided to switch my box!")
        if final_choice.has_car:
            print(f"Host: Congratulations {player.name}, you have won a car!")
        else:
            print(f"Host: Sorry {player.name}, you have won the goat.")
    return round_result