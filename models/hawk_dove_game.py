from .core import GameModel

class HawkDoveGame(GameModel):
    name = "Hawk-Dove Game"
    description = "A classic conflict model examining aggressive vs. passive behavior, also known as Chicken Game. Players can be aggressive (Hawk) or passive (Dove), with different outcomes depending on their choices."
    row_labels = ["Hawk", "Dove"]
    col_labels = ["Hawk", "Dove"]

    def __init__(self, value=4, cost=6):
        super().__init__({'value': value, 'cost': cost})

    def play(self, action1, action2):
        # action: 0=Hawk, 1=Dove
        value, cost = self.params['value'], self.params['cost']
        
        if action1 == 0 and action2 == 0:
            # Both Hawk - they fight and split the value, but both incur cost
            return (value - cost)/2, (value - cost)/2
        elif action1 == 0 and action2 == 1:
            # Player 1 Hawk, Player 2 Dove - Hawk gets all value, Dove retreats
            return value, 0
        elif action1 == 1 and action2 == 0:
            # Player 1 Dove, Player 2 Hawk - Hawk gets all value, Dove retreats
            return 0, value
        else:  # Both Dove
            # Both share the value peacefully
            return value/2, value/2
