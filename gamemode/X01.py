from kivy.uix.popup import Popup
from gamemode.player import Player
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivymd.uix.boxlayout import BoxLayout


class X01():
    # create the game
    def __init__(self, score=101):
        super()
        self.players = []
        self.game_score = score
        self.double_out = True
        self.current_player_index = 0

    # add new player
    def add_player(self, name):
        player = Player(name, self.game_score)
        self.players.append(player)

    # set score of current player and handle next step
    def score_hit(self, score_string):
        player = self.players[self.current_player_index]
        next_player_name = self.get_next_player_name()
        # check if first darts thrown
        if player.current_darts_thrown == 3:
            player.last_three_points.clear()
            player.current_score = 0
            player.current_darts_thrown = 0

        score = self.string_to_score(score_string)
        if player.game_score-score < 0 or (player.game_score-score == 1 and self.double_out):
            self.player_overthrow(player, score_string)
            return player, next_player_name, True, False
        elif player.game_score-score == 0:
            if self.double_out:
                if score_string[0] == 'D':
                    self.player_won(player)
                    print(player.name + "won the game")
                    return player, next_player_name, False, True
                else:
                    self.player_overthrow(player, score_string)
                    print(player.name + " has not hit double out")
                    return player, next_player_name, True, False
            else:
                print(player.name + "won the game")
                self.player_won(player)
                return player, next_player_name, False, True
        # normal hit
        else:
            # game status
            player.game_score -= score
            # satistics
            player.current_score += score
            player.total_darts_thrown += 1
            player.last_three_points.append(score_string)
            player.current_darts_thrown += 1
            player.total_score += score

            # check if 3 darts are thrown
            if len(player.last_three_points) == 3:
                self.next_player(player)
        return player, next_player_name, False, False

    # reset player to last score and change to next player
    def player_overthrow(self, player, score_string):
        if len(player.last_three_points) != 0:
            for score in player.last_three_points:
                player.game_score += self.string_to_score(score)
                player.total_score -= self.string_to_score(score)

        player.current_score += self.string_to_score(score_string)
        player.total_darts_thrown += 1
        player.last_three_points.append(score_string)
        player.current_darts_thrown = 3
        self.next_player(player)

    # set current_player index to next player
    def next_player(self, player):
        if self.current_player_index == len(self.players)-1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1

    # get the name of the next player
    def get_next_player_name(self):
        if self.current_player_index == len(self.players)-1:
            return self.players[0].name
        else:
            return self.players[self.current_player_index+1].name

    # remove existing player
    def remove_player(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
                return

    # convert score as string to int
    def string_to_score(self, score):
        s0 = score[0]
        if s0 == '-':
            return 0
        if s0 == 'D':
            return 2*int(score[1:])
        if s0 == 'T':
            return 3*int(score[1:])
        return int(score)

    # shows winner screen and resets game
    def player_won(self, player):
        layout = BoxLayout(orientation="vertical")
        label = MDLabel(text=player.name + " has won the game")
        button = Button(text='Okay')
        layout.add_widget(label)
        layout.add_widget(button)
        popup = Popup(title='Game over',
                      content=layout,
                      size_hint=(None, None), size=(400, 200))

        button.bind(on_press=popup.dismiss)
        popup.open()

    def has_game_started(self):
        if len(self.players) > 0:
            if self.players[0].current_darts_thrown == 0:
                return False
            return True
