from .core import GameModel

class BattleOfSexes(GameModel):
    name = "Battle of Sexes"
    description = "A coordination game representing conflict of interest between two players who need to coordinate but have different preferences for the activity they choose."
    row_labels = ["Opera", "Football"]
    col_labels = ["Opera", "Football"]

    def __init__(self, opera_man=2, opera_woman=1, football_man=1, football_woman=2):
        super().__init__({
            'opera_man': opera_man, 
            'opera_woman': opera_woman,
            'football_man': football_man,
            'football_woman': football_woman
        })

    def play(self, action1, action2):
        # action for man: 0=Opera, 1=Football
        # action for woman: 0=Opera, 1=Football
        opera_man = self.params['opera_man']
        opera_woman = self.params['opera_woman']
        football_man = self.params['football_man']
        football_woman = self.params['football_woman']
        
        if action1 == 0 and action2 == 0:
            # Both choose Opera
            return opera_man, opera_woman
        elif action1 == 1 and action2 == 1:
            # Both choose Football
            return football_man, football_woman
        else:
            # They go to different activities - both get 0
            return 0, 0
