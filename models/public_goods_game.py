from .core import GameModel
import numpy as np

class PublicGoodsGame(GameModel):
    name = "Public Goods Game"
    description = "A multiplayer game where players decide how much to contribute to a public pot that benefits everyone, exploring the tension between individual and group interests."

    def __init__(self, endowment=10, multiplier=1.6, num_players=4):
        super().__init__({'endowment': endowment, 'multiplier': multiplier, 'num_players': num_players})
        
    def play(self, contributions):
        # contributions: list of contributions from each player
        endowment = self.params['endowment']
        multiplier = self.params['multiplier']
        num_players = self.params['num_players']
        
        # Validate contributions
        contributions = np.clip(contributions, 0, endowment)
        
        # Calculate total contribution and return for each player
        total_contribution = sum(contributions)
        public_good = total_contribution * multiplier
        individual_return = public_good / num_players
        
        # Calculate final payoffs
        payoffs = [endowment - contrib + individual_return for contrib in contributions]
        
        return payoffs
        
    def play_two_player(self, contrib1, contrib2):
        # Simplified version for two players in the web interface
        endowment = self.params['endowment']
        multiplier = self.params['multiplier']
        
        # Validate contributions
        contrib1 = min(max(0, contrib1), endowment)
        contrib2 = min(max(0, contrib2), endowment)
        
        # Calculate total contribution and return
        total_contribution = contrib1 + contrib2
        public_good = total_contribution * multiplier
        individual_return = public_good / 2
        
        # Calculate final payoffs
        payoff1 = endowment - contrib1 + individual_return
        payoff2 = endowment - contrib2 + individual_return
        
        return payoff1, payoff2
