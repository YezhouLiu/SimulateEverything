from .core import GameModel
import numpy as np

class RepeatedPrisonersDilemma(GameModel):
    name = "Repeated Prisoner's Dilemma"
    description = "A multi-round version of Prisoner's Dilemma where players can learn and adapt strategies over time, exploring cooperation emergence."
    row_labels = ["Cooperate", "Betray"]
    col_labels = ["Cooperate", "Betray"]

    def __init__(self, R=3, T=5, S=0, P=1, rounds=5, discount_factor=0.9):
        super().__init__({
            'R': R, 
            'T': T, 
            'S': S, 
            'P': P, 
            'rounds': rounds,
            'discount_factor': discount_factor
        })
        
    def play_single_round(self, action1, action2):
        """Play a single round of Prisoner's Dilemma"""
        R, T, S, P = self.params['R'], self.params['T'], self.params['S'], self.params['P']
        if action1 == 0 and action2 == 0:
            return R, R
        elif action1 == 1 and action2 == 1:
            return P, P
        elif action1 == 0 and action2 == 1:
            return S, T
        else:
            return T, S
    
    def play_with_strategies(self, strategy1, strategy2):
        """
        Play repeated game with given strategies
        
        Strategies:
        0: Always Cooperate
        1: Always Betray
        2: Tit-for-Tat (start cooperating, then copy opponent's last move)
        3: Suspicious Tit-for-Tat (start betraying, then copy opponent's last move)
        4: Pavlov (win-stay, lose-shift)
        """
        rounds = self.params['rounds']
        discount = self.params['discount_factor']
        
        # Initialize history and scores
        history1 = []  # Player 1's moves
        history2 = []  # Player 2's moves
        total_score1 = 0
        total_score2 = 0
        
        for r in range(rounds):
            # Determine actions based on strategies
            if r == 0:  # First round
                if strategy1 == 0 or strategy1 == 2:  # Always Cooperate or Tit-for-Tat
                    action1 = 0  # Cooperate
                else:  # Always Betray or Suspicious Tit-for-Tat or Pavlov
                    action1 = 1  # Betray
                    
                if strategy2 == 0 or strategy2 == 2:  # Always Cooperate or Tit-for-Tat
                    action2 = 0  # Cooperate
                else:  # Always Betray or Suspicious Tit-for-Tat or Pavlov
                    action2 = 1  # Betray
            else:  # Subsequent rounds
                if strategy1 == 0:  # Always Cooperate
                    action1 = 0
                elif strategy1 == 1:  # Always Betray
                    action1 = 1
                elif strategy1 == 2 or strategy1 == 3:  # Tit-for-Tat or Suspicious Tit-for-Tat
                    action1 = history2[-1]  # Copy opponent's last move
                elif strategy1 == 4:  # Pavlov
                    # If last round was good (CC or DC), repeat action; otherwise change
                    if (history1[-1] == 0 and history2[-1] == 0) or (history1[-1] == 1 and history2[-1] == 0):
                        action1 = history1[-1]  # Repeat
                    else:
                        action1 = 1 - history1[-1]  # Change
                
                if strategy2 == 0:  # Always Cooperate
                    action2 = 0
                elif strategy2 == 1:  # Always Betray
                    action2 = 1
                elif strategy2 == 2 or strategy2 == 3:  # Tit-for-Tat or Suspicious Tit-for-Tat
                    action2 = history1[-1]  # Copy opponent's last move
                elif strategy2 == 4:  # Pavlov
                    # If last round was good (CC or DC), repeat action; otherwise change
                    if (history2[-1] == 0 and history1[-1] == 0) or (history2[-1] == 1 and history1[-1] == 0):
                        action2 = history2[-1]  # Repeat
                    else:
                        action2 = 1 - history2[-1]  # Change
            
            # Play the round
            score1, score2 = self.play_single_round(action1, action2)
            
            # Apply discount factor
            discount_multiplier = discount ** r
            total_score1 += score1 * discount_multiplier
            total_score2 += score2 * discount_multiplier
              # Update history
            history1.append(action1)
            history2.append(action2)
        
        return {
            "scores": [total_score1, total_score2],
            "history1": history1,
            "history2": history2
        }

    def play(self, strategy1, strategy2):
        """Simple interface for playing the game with strategies"""
        result = self.play_with_strategies(strategy1, strategy2)
        return result["scores"]
    
    def get_strategy_name(self, strategy):
        """Return the name of a strategy"""
        strategy_names = {
            0: "Always Cooperate",
            1: "Always Betray",
            2: "Tit-for-Tat",
            3: "Suspicious Tit-for-Tat",
            4: "Pavlov (Win-Stay, Lose-Shift)"
        }
        return strategy_names.get(strategy, "Unknown Strategy")
