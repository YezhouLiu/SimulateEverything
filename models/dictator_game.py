from .core import GameModel
import numpy as np

class DictatorGame(GameModel):
    name = "Dictator Game"
    description = "A simple economic game exploring fairness and altruism. One player (the dictator) decides how to split a sum of money with another player who has no choice but to accept."

    def __init__(self, total_amount=10):
        super().__init__({'total_amount': total_amount})
        
    def play(self, amount_given):
        # amount_given: how much dictator gives to the recipient (0-total_amount)
        total_amount = self.params['total_amount']
        
        # Validate input
        amount_given = min(max(0, amount_given), total_amount)
        
        # Calculate final payoffs
        payoff_dictator = total_amount - amount_given
        payoff_recipient = amount_given
        
        return payoff_dictator, payoff_recipient
