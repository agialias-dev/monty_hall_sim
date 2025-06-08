class Box():
    def __init__(self, number, is_winner = False):
        self.number = number
        self.is_winner = is_winner
        self.is_opened = False
        self.is_chosen = False

    def __repr__(self):
        return f"Box number:{self.number} is winner={self.is_winner}"
