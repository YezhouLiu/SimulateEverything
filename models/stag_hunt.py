from .core import GameModel

class StagHunt(GameModel):
    name = "Stag Hunt"
    description = "A game model with both cooperation and risk, examining trust and collaboration."
    row_labels = ["Hunt Stag", "Hunt Hare"]
    col_labels = ["Hunt Stag", "Hunt Hare"]

    def __init__(self, stag=4, hare=2, fail=0):
        super().__init__({'stag': stag, 'hare': hare, 'fail': fail})

    def play(self, action1, action2):
        # action: 0=Hunt Stag, 1=Hunt Hare
        stag, hare, fail = self.params['stag'], self.params['hare'], self.params['fail']
        if action1 == 0 and action2 == 0:
            return stag, stag
        elif action1 == 1 and action2 == 1:
            return hare, hare
        elif action1 == 0 and action2 == 1:
            return fail, hare
        else:
            return hare, fail
