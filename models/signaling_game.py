from .core import GameModel
import numpy as np

class SignalingGame(GameModel):
    name = "Signaling Game"
    description = "An asymmetric information game where one player knows their type and can send a signal, while the other player must interpret this signal and respond. Models communication when incentives aren't fully aligned."

    def __init__(self, high_sender_high_signal_payoff=10, high_sender_low_signal_payoff=5,
                 low_sender_high_signal_payoff=8, low_sender_low_signal_payoff=7,
                 correct_receiver_payoff=6, incorrect_receiver_payoff=2,
                 high_type_probability=0.5):
        super().__init__({
            'high_sender_high_signal_payoff': high_sender_high_signal_payoff, 
            'high_sender_low_signal_payoff': high_sender_low_signal_payoff,
            'low_sender_high_signal_payoff': low_sender_high_signal_payoff, 
            'low_sender_low_signal_payoff': low_sender_low_signal_payoff,
            'correct_receiver_payoff': correct_receiver_payoff,
            'incorrect_receiver_payoff': incorrect_receiver_payoff,
            'high_type_probability': high_type_probability
        })
    
    def play(self, sender_strategy, receiver_strategy):
        """
        Play the signaling game
        
        sender_strategy: 
            0 = Separating (High type sends High signal, Low type sends Low signal)
            1 = Pooling High (Both types send High signal)
            2 = Pooling Low (Both types send Low signal)
            3 = Perverse (High type sends Low signal, Low type sends High signal)
        
        receiver_strategy:
            0 = Trust (Believe the signal: High signal -> High action, Low signal -> Low action)
            1 = Distrust (Opposite of signal: High signal -> Low action, Low signal -> High action)
            2 = Always High (Always take High action regardless of signal)
            3 = Always Low (Always take Low action regardless of signal)
        """
        # For calculating expected payoffs, we need to consider probabilities
        high_type_prob = self.params['high_type_probability']
        low_type_prob = 1 - high_type_prob
        
        # Payoff parameters
        high_high = self.params['high_sender_high_signal_payoff']
        high_low = self.params['high_sender_low_signal_payoff']
        low_high = self.params['low_sender_high_signal_payoff']
        low_low = self.params['low_sender_low_signal_payoff']
        correct = self.params['correct_receiver_payoff']
        incorrect = self.params['incorrect_receiver_payoff']
        
        # Initialize expected payoffs
        sender_payoff = 0
        receiver_payoff = 0
        
        # Map sender strategy to signals
        if sender_strategy == 0:  # Separating
            high_type_signal = 1  # High signal
            low_type_signal = 0   # Low signal
        elif sender_strategy == 1:  # Pooling High
            high_type_signal = 1  # High signal
            low_type_signal = 1   # High signal
        elif sender_strategy == 2:  # Pooling Low
            high_type_signal = 0  # Low signal
            low_type_signal = 0   # Low signal
        elif sender_strategy == 3:  # Perverse
            high_type_signal = 0  # Low signal
            low_type_signal = 1   # High signal
        else:
            raise ValueError("Invalid sender strategy")
        
        # Calculate expected payoffs for High type
        if high_type_signal == 1:  # High type sends High signal
            if receiver_strategy == 0:  # Trust: High signal -> High action
                sender_payoff += high_type_prob * high_high
                receiver_payoff += high_type_prob * correct
            elif receiver_strategy == 1:  # Distrust: High signal -> Low action
                sender_payoff += high_type_prob * high_low
                receiver_payoff += high_type_prob * incorrect
            elif receiver_strategy == 2:  # Always High
                sender_payoff += high_type_prob * high_high
                receiver_payoff += high_type_prob * correct
            elif receiver_strategy == 3:  # Always Low
                sender_payoff += high_type_prob * high_low
                receiver_payoff += high_type_prob * incorrect
        else:  # High type sends Low signal
            if receiver_strategy == 0:  # Trust: Low signal -> Low action
                sender_payoff += high_type_prob * high_low
                receiver_payoff += high_type_prob * incorrect
            elif receiver_strategy == 1:  # Distrust: Low signal -> High action
                sender_payoff += high_type_prob * high_high
                receiver_payoff += high_type_prob * correct
            elif receiver_strategy == 2:  # Always High
                sender_payoff += high_type_prob * high_high
                receiver_payoff += high_type_prob * correct
            elif receiver_strategy == 3:  # Always Low
                sender_payoff += high_type_prob * high_low
                receiver_payoff += high_type_prob * incorrect
        
        # Calculate expected payoffs for Low type
        if low_type_signal == 1:  # Low type sends High signal
            if receiver_strategy == 0:  # Trust: High signal -> High action
                sender_payoff += low_type_prob * low_high
                receiver_payoff += low_type_prob * incorrect
            elif receiver_strategy == 1:  # Distrust: High signal -> Low action
                sender_payoff += low_type_prob * low_low
                receiver_payoff += low_type_prob * correct
            elif receiver_strategy == 2:  # Always High
                sender_payoff += low_type_prob * low_high
                receiver_payoff += low_type_prob * incorrect
            elif receiver_strategy == 3:  # Always Low
                sender_payoff += low_type_prob * low_low
                receiver_payoff += low_type_prob * correct
        else:  # Low type sends Low signal
            if receiver_strategy == 0:  # Trust: Low signal -> Low action
                sender_payoff += low_type_prob * low_low
                receiver_payoff += low_type_prob * correct
            elif receiver_strategy == 1:  # Distrust: Low signal -> High action
                sender_payoff += low_type_prob * low_high
                receiver_payoff += low_type_prob * incorrect
            elif receiver_strategy == 2:  # Always High
                sender_payoff += low_type_prob * low_high
                receiver_payoff += low_type_prob * incorrect
            elif receiver_strategy == 3:  # Always Low
                sender_payoff += low_type_prob * low_low
                receiver_payoff += low_type_prob * correct
        
        return sender_payoff, receiver_payoff
    
    def get_sender_strategy_name(self, strategy):
        """Return the name of a sender strategy"""
        strategy_names = {
            0: "Separating (Honest)",
            1: "Pooling High",
            2: "Pooling Low",
            3: "Perverse (Dishonest)"
        }
        return strategy_names.get(strategy, "Unknown Strategy")
    
    def get_receiver_strategy_name(self, strategy):
        """Return the name of a receiver strategy"""
        strategy_names = {
            0: "Trust Signals",
            1: "Distrust Signals",
            2: "Always High",
            3: "Always Low"
        }
        return strategy_names.get(strategy, "Unknown Strategy")
