from .core import GameModel

class TrustGame(GameModel):
    name = "Trust Game"
    description = "An economic game exploring trust and reciprocity. The first player decides how much to send to the second, this amount is multiplied, and the second player decides how much to return."

    def __init__(self, initial_amount=10, multiplier=3):
        super().__init__({'initial_amount': initial_amount, 'multiplier': multiplier})
        
    def play(self, amount_sent, amount_returned_ratio):
        # amount_sent: how much first player sends (0-initial_amount)
        # amount_returned_ratio: proportion second player returns (0-1)
        initial_amount = self.params['initial_amount']
        multiplier = self.params['multiplier']
        
        # Validate inputs
        amount_sent = min(max(0, amount_sent), initial_amount)
        amount_returned_ratio = min(max(0, amount_returned_ratio), 1)
        
        # Calculate the multiplied amount
        multiplied_amount = amount_sent * multiplier
        
        # Calculate how much is returned
        amount_returned = multiplied_amount * amount_returned_ratio
        
        # Calculate final payoffs
        payoff_sender = initial_amount - amount_sent + amount_returned
        payoff_receiver = multiplied_amount - amount_returned
        
        return payoff_sender, payoff_receiver
        
    def play_simple(self, send_choice, return_choice):
        # Simplified version for the web interface
        # send_choice: 0=Low Trust, 1=Medium Trust, 2=High Trust
        # return_choice: 0=Low Return, 1=Medium Return, 2=High Return
        
        initial_amount = self.params['initial_amount']
        multiplier = self.params['multiplier']
        
        # Map choices to actual amounts
        send_amounts = {
            0: initial_amount * 0.2,  # Low
            1: initial_amount * 0.5,  # Medium
            2: initial_amount * 0.8   # High
        }
        
        return_ratios = {
            0: 0.1,  # Low
            1: 0.3,  # Medium
            2: 0.5   # High
        }
        
        amount_sent = send_amounts[send_choice]
        return_ratio = return_ratios[return_choice]
        
        return self.play(amount_sent, return_ratio)
