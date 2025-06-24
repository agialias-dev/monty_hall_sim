import random
from enum import Enum

class Name(Enum):
    ALEX = "Alex"
    BOB = "Bob"
    CAROL = "Carol"
    DAVE = "Dave"
    EVE = "Eve"
    FRANK = "Frank"
    GRACE = "Grace"
    HEIDI = "Heidi"
    IVAN = "Ivan"
    JUDY = "Judy"
    GILES = "Giles"
    HELEN = "Helen"
    LUCY = "Lucy"
    GUY = "Guy"
    ELIZABETH = "Elizabeth"
    KATE = "Kate"

class Player():
    def __init__(self, will_switch):
        self.will_switch = will_switch
        self.first_choice = None
        self.final_choice = None
        self.name = random.choice(list(Name)).value
    
    def choose_box(self, boxes):
        self.first_choice = random.SystemRandom().choice(boxes)
        return self.first_choice
     
    def keep_or_switch(self, boxes):
        if self.will_switch:
            available_boxes = [box for box in boxes if box != self.first_choice and not box.is_opened]
            chosen_box = random.SystemRandom().choice(available_boxes)
            chosen_box.is_chosen = True
            chosen_box.is_opened = True
            self.final_choice = chosen_box
        else:
            self.final_choice = self.first_choice
        return self.final_choice