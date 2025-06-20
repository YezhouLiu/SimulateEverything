from .core import GameModel

class PrisonersDilemma(GameModel):
    name = "Prisoner's Dilemma"
    description = "A classic non-zero-sum game model where two prisoners choose to cooperate or betray."
    row_labels = ["Cooperate", "Betray"]
    col_labels = ["Cooperate", "Betray"]

    def __init__(self, R=3, T=5, S=0, P=1):
        super().__init__({'R': R, 'T': T, 'S': S, 'P': P})

    def play(self, action1, action2):
        # action: 0=Cooperate, 1=Betray
        R, T, S, P = self.params['R'], self.params['T'], self.params['S'], self.params['P']
        if action1 == 0 and action2 == 0:
            return R, R
        elif action1 == 1 and action2 == 1:
            return P, P
        elif action1 == 0 and action2 == 1:
            return S, T
        else:
            return T, S
