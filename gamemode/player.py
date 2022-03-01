class Player():
    def __init__(self, name, game_score):
        self.name = name
        self.game_score = game_score
        self.total_score = 0
        self.current_score = 0
        self.total_darts_thrown = 0
        self.last_three_points = []


    def get_avrg(self):
        return round(self.total_score/self.total_darts_thrown, 2)

    def get_current_index(self):
        return len(self.last_three_points)-1
    
