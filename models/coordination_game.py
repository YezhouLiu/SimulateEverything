from .core import GameModel

class CoordinationGame(GameModel):
    name = "Coordination Game"
    description = "A game where players benefit from coordinating their actions, demonstrating the importance of coordination in social situations."

    def __init__(self, coord_a=3, coord_b=3, mismatch=0):
        super().__init__({'coord_a': coord_a, 'coord_b': coord_b, 'mismatch': mismatch})

    def play(self, action1, action2):
        # action: 0=Option A, 1=Option B
        coord_a, coord_b, mismatch = self.params['coord_a'], self.params['coord_b'], self.params['mismatch']
        if action1 == 0 and action2 == 0:
            return coord_a, coord_a
        elif action1 == 1 and action2 == 1:
            return coord_b, coord_b
        else:
            return mismatch, mismatch
