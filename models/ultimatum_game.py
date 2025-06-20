from .core import GameModel
import numpy as np

class UltimatumGame(GameModel):
    name = "Ultimatum Game"
    description = "A negotiation game where one player proposes how to divide a sum of money, and the other player can accept or reject the offer. If rejected, both players receive nothing."

    def __init__(self, total_amount=10):
        super().__init__({
            'total_amount': total_amount
        })
    
    def play(self, offer_amount, accept_threshold):
        """
        Play the Ultimatum Game
        
        offer_amount: Amount offered by the proposer (0 to total_amount)
        accept_threshold: Minimum amount the responder will accept (0 to total_amount)
        
        Returns the payoffs for both players
        """
        total = self.params['total_amount']
        
        # Validate inputs
        offer_amount = min(max(0, offer_amount), total)
        accept_threshold = min(max(0, accept_threshold), total)
        
        # Determine if the offer is accepted
        if offer_amount >= accept_threshold:
            # Offer accepted
            proposer_payoff = total - offer_amount
            responder_payoff = offer_amount
        else:
            # Offer rejected
            proposer_payoff = 0
            responder_payoff = 0
        
        return proposer_payoff, responder_payoff
    
    def play_with_strategy(self, proposer_strategy, responder_strategy):
        """
        Play the game with predefined strategies
        
        proposer_strategy:
            0 = Fair Split (50%)
            1 = Slightly Unfair (30%)
            2 = Very Unfair (10%)
            3 = Almost All (90%)
        
        responder_strategy:
            0 = Accept Anything
            1 = Require Fair (50%+)
            2 = Require Somewhat Fair (30%+)
            3 = Rational (Accept any non-zero)
        
        Returns the payoffs for both players
        """
        total = self.params['total_amount']
        
        # Determine offer based on proposer strategy
        if proposer_strategy == 0:  # Fair Split
            offer = total // 2
        elif proposer_strategy == 1:  # Slightly Unfair
            offer = total * 0.3
        elif proposer_strategy == 2:  # Very Unfair
            offer = total * 0.1
        elif proposer_strategy == 3:  # Almost All
            offer = total * 0.9
        else:
            raise ValueError("Invalid proposer strategy")
        
        # Determine acceptance threshold based on responder strategy
        if responder_strategy == 0:  # Accept Anything
            threshold = 0
        elif responder_strategy == 1:  # Require Fair
            threshold = total * 0.5
        elif responder_strategy == 2:  # Require Somewhat Fair
            threshold = total * 0.3
        elif responder_strategy == 3:  # Rational
            threshold = 1 if total > 0 else 0  # Accept any non-zero
        else:
            raise ValueError("Invalid responder strategy")
        
        # Round to integers if necessary
        offer = round(offer)
        threshold = round(threshold)
        
        return self.play(offer, threshold)
    
    def get_proposer_strategy_name(self, strategy):
        """Return the name of a proposer strategy"""
        strategy_names = {
            0: "Fair Split (50%)",
            1: "Slightly Unfair (30%)",
            2: "Very Unfair (10%)",
            3: "Almost All (90%)"
        }
        return strategy_names.get(strategy, "Unknown Strategy")
    
    def get_responder_strategy_name(self, strategy):
        """Return the name of a responder strategy"""
        strategy_names = {
            0: "Accept Anything",
            1: "Require Fair (50%+)",
            2: "Require Somewhat Fair (30%+)",
            3: "Rational (Accept any non-zero)"
        }
        return strategy_names.get(strategy, "Unknown Strategy")
