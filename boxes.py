class Box():
    def __init__(self, number, has_car = False):
        self.number = number
        self.has_car = has_car
        self.is_opened = False
        self.is_chosen = False

    def __str__(self):
        return f"Box number:{self.number} has a {'car' if self.has_car else 'goat'}"
    
    def __repr__(self):
        return f"Box(number={self.number}, has_car={self.has_car}, is_opened={self.is_opened}, is_chosen={self.is_chosen})"
    
    def __bool__(self):
        return self.has_car == True