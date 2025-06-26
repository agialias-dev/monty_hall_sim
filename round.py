import random
from boxes import Box
from players import Player

def play_round(player_type, verbose):
# Args:
#   player_type (bool): If True, the player will switch boxes; if False, they will keep their initial choice.
#   verbose (bool): if enabled prints enhanced information.
    
    # Verbosity switches
    if verbose == 1:
        def v1print(print_data):
            print(print_data)
        def v2print(print_data):
            pass
    elif verbose == 2:
        def v1print(print_data):
            print(print_data)
        def v2print(print_data):
            print(print_data)
    else:
        def v1print(print_data):
            pass
        def v2print(print_data):
            pass
    
    # Initialize Player
    player = Player(player_type)
    v2print(f"\nDEBUG: {repr(player)}\n")
    v1print(f"Host: Welcome {player.name}, to Keep OR Switch!")

    # Generate 3 boxes.
    boxes = [Box(_) for _ in range(1, 4)]
    winning_box = random.SystemRandom().choice(boxes)
    winning_box.has_car = True
    v2print(f"\nDEBUG: {boxes}\n")

    # Player picks their first box.
    v1print(f"Host: I have placed a car in one of these three boxes, the other two contain a goat. {player.name}, please choose a box.")
    chosen_box = player.choose_box(boxes)
    chosen_box.is_chosen = True
    v2print(f"\nDEBUG: Chosen box = {repr(chosen_box)}\n")
    v1print(f"{player.name}: I would like box number {chosen_box.number} please.")

    # Host Eliminates a losing box.
    for box in boxes:
        if box.is_chosen == False and box.has_car == False:
            box.is_opened = True
            v1print(f"Host: I can reveal that box number {box.number} had a {'car' if box.has_car else 'goat'} inside it, and I will now remove it from the game.")
            v2print(f"\nDEBUG: Host removed {repr(box)}\n")
            boxes.remove(box)
            break

    # Player chooses to keep or switch.
    v1print(f"Host: Now, {player.name}, you have the option to keep your original box or switch to the remaining box.")
    v2print(f"\nDEBUG: {boxes}\n")
    final_choice = player.keep_or_switch(boxes)

    # Result of the round
    round_result = final_choice.has_car
    v2print(f"\nDEBUG: Final choice is {repr(final_choice)}\n")
    if final_choice == player.first_choice:
        v1print(f"{player.name}: I have decided to keep my box.") 
        if final_choice.has_car:
            v1print(f"Host: Congratulations {player.name}, you have won a car!")
        else:
            v1print(f"Host: Sorry {player.name}, you have won the goat.")
        return round_result
    else:
        v1print(f"{player.name}: I have decided to switch my box!")
        if final_choice.has_car:
            v1print(f"Host: Congratulations {player.name}, you have won a car!")
        else:
            v1print(f"Host: Sorry {player.name}, you have won the goat.")
    return round_result