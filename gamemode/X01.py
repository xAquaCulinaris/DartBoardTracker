from gamemode.player import Player


class X01():
    #create the game
    def __init__(self, score = 501):
        super()
        self.players = []
        self.game_score = score
        self.double_out = True
        self.current_player_index = 0

        
    #add new player
    def add_player(self, name):
        player = Player(name, self.game_score)
        self.players.append(player)

    #restart the game
    def reset_game(self):
        for player in self.players:
            player.total_score = 0
            player.current_score = 0
            player.total_darts_thrown = 0
            player.last_three_point = []

    #set score of current player and handle next step
    def score_hit(self, score_string):
        player = self.players[self.current_player_index]
        next_player_name = self.get_next_player_name()
        #check if first darts thrown
        if len(player.last_three_points) == 3:
            player.last_three_points.clear()
            player.current_score = 0

        score = self.string_to_score(score_string)
        if player.game_score-score < 0:
            self.player_overthrow(player)
        elif player.game_score-score == 0:
            if self.double_out:
                if score_string[0] == 'D':
                    print(player.name + "has won the game")
                else:
                    self.player_overthrow(player)
                    self.next_player(player)
                    print(player.name + " has not hit double out")
            else:
                print(player.name + "has won the game")
        #normal hit
        else:
            #game status
            player.game_score -= score
            #satistics
            player.current_score += score
            player.total_darts_thrown += 1
            player.last_three_points.append(score_string)
            player.total_score += score
            player.total_darts_thrown += 1

            #check if 3 darts are thrown
            if len(player.last_three_points) == 3:
                self.next_player(player)
        return player, next_player_name

    #reset player to last score and change to next player
    def player_overthrow(self, player):
        if len(player.last_three_points) != 0:
            for score in player.last_three_points:
                player.game_score += self.string_to_score(score)
                player.total_score -= self.string_to_score(score)
        self.next_player(player)

    #set current_player index to next player
    def next_player(self, player):
        if self.current_player_index == len(self.players)-1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1

    def get_next_player_name(self):
        if self.current_player_index == len(self.players)-1:
            return self.players[0].name
        else:
            return self.players[self.current_player_index+1].name 
            

    
    #remove existing player
    def remove_player(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
                return

    def string_to_score(self, score):
        s0 = score[0]
        if s0 == '-':
            return 0
        if s0 == 'D':
            return 2*int(score[1:])
        if s0 == 'T':
            return 3*int(score[1:])
        return int(score)



    
