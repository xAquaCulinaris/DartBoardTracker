from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.button import MDTextButton
from kivymd.uix.menu import MDDropdownMenu
import random
import cv2
import os.path

from gamemode.X01 import X01
from gui.player_widget import PlayerWidget


Window.size = (1000, 600)


class DartboardGui(MDApp):
    # build inital screen
    def build(self):
        self.screen = Builder.load_file('gui/main.kv')
        self.player_names = []
        self.available_players_labes = []
        self.current_players = []
        self.load_player_names_from_file()

        # register double out switch
        double_out_button = self.screen.ids.double_out_checkbox
        double_out_button.bind(active=self.on_double_out_switched)

        # add items to game score dropdown menu
        menu_names = ["301", "501", "701", "901"]
        menu_items = [
            {
                "text": menu_names[i],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=menu_names[i]: self.menu_callback(x),
            } for i in range(4)
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.dropdown_menu,
            items=menu_items,
            width_mult=4,
        )

        self.gamemode = X01(101)

        return self.screen

    # get obj of a list of x.text objects
    def get_object_by_name(self, name, list):
        for obj in list:
            if obj.text == name:
                return obj
        return None

    # add player button pressed
    def add_player_pressed(self):
        # get name from textbox
        name = self.screen.ids.add_player_text.text
        # check that name is not empty and not already in currentplayer
        if not name == "" and self.get_player_from_list(name, self.current_players) == None:
            self.add_player_to_main_screen(name)
            # add player to current player menue
            mdButton = MDTextButton(text=name)
            mdButton.bind(on_press=self.remove_label_from_current)
            self.screen.ids.current_players_grid.add_widget(mdButton)

            # if player in available list remove it
            mdLabel = self.get_object_by_name(
                name, self.available_players_labes)
            if mdLabel:
                self.screen.ids.available_players_grid.remove_widget(mdLabel)

            # if name not already exists add name to file
            if not name in self.player_names:
                self.write_player_name_to_file(name)

        self.screen.ids.add_player_text.text = ""

    def get_player_from_list(self, name, list):
        for player in list:
            if player.name == name:
                return player
        return None

    # writes a new player name to a file to save it permanently
    def write_player_name_to_file(self, name):
        # open file
        player_names_file = open('assets/data/player_names.txt', 'a')
        # write name
        player_names_file.write(name+"\n")
        # close file
        player_names_file.close()
        # add name to list of all names
        self.player_names.append(name)

    # loads permanent players from file
    def load_player_names_from_file(self):
        if os.path.isfile('assets/data/player_names.txt'):
            # open file
            player_names_file = open('assets/data/player_names.txt', 'r')
            # get all lines
            names = player_names_file.readlines()
            # loop over each line
            for name in names:
                # add player name to list of players
                test = name.rstrip("\n")
                self.player_names.append(name.rstrip("\n"))
                # add label to available players
                label = MDTextButton(text=name.rstrip("\n"))
                label.bind(on_press=self.remove_label_from_avilable)
                self.available_players_labes.append(label)
                self.screen.ids.available_players_grid.add_widget(label)
            player_names_file.close()

    # on button press removes label from list of available players
    def remove_label_from_avilable(self, button):
        self.screen.ids.available_players_grid.remove_widget(button)
        button.unbind(on_press=self.remove_label_from_avilable)
        button.bind(on_press=self.remove_label_from_current)
        self.screen.ids.current_players_grid.add_widget(button)
        # add player to main screen
        self.add_player_to_main_screen(button.text)

    # on button press remove label from list of current players
    def remove_label_from_current(self, button):
        # remove player from current players
        self.screen.ids.current_players_grid.remove_widget(button)
        # rebind button press
        button.unbind(on_press=self.remove_label_from_current)
        button.bind(on_press=self.remove_label_from_avilable)
        # add player to avaible palyers
        self.screen.ids.available_players_grid.add_widget(button)
        # remove player from main screen
        player = self.get_player_from_list(button.text, self.current_players)
        self.screen.ids.player_grid.remove_widget(player.main_layout)
        self.current_players.remove(player)
        # remove player from gamemode
        self.gamemode.remove_player(player.name)

    def add_player_to_main_screen(self, name):
        player = PlayerWidget(name, self.gamemode.game_score)
        if len(self.current_players) == 0:
            player.main_layout.update_color(True)
        else:
            player.main_layout.update_color(False)
        self.current_players.append(player)
        self.screen.ids.player_grid.add_widget(player.main_layout)
        self.gamemode.add_player(name)

    def generate_test_data_pressed(self):
        if len(self.current_players) > 0:
            # generate random point
            test_point = self.dartboard.get_random_point()
            score = self.dartboard.check_point(test_point)

            current_player, next_player_name, over_throw, game_over = self.gamemode.score_hit(
                score)

            if game_over:
                self.restart_game()
            else:
                current_player_widget = self.get_player_widget_by_name(
                    current_player.name)
                next_player_widget = self.get_player_widget_by_name(
                    next_player_name)
                current_player_widget.update_score(current_player, over_throw)
                if current_player.current_darts_thrown == 3:
                    next_player_widget.clear_score()
                    next_player_widget.main_layout.update_color()

                # draw point to the image
                if len(current_player.last_three_points) == 1:
                    dartboard_img = self.dartboard.draw_point_on_board(
                        test_point, True)
                else:
                    dartboard_img = self.dartboard.draw_point_on_board(
                        test_point, False)
                cv2.imwrite("assets/images/dartboard_hit.png", dartboard_img)
                self.screen.ids.dartboard_img.source = "assets/images/dartboard_hit.png"
                self.screen.ids.dartboard_img.reload()

    def shuffle_players(self):
        if len(self.current_players) > 0:
            if self.gamemode.players[0].total_darts_thrown == 0:
                # remove players
                for player in self.current_players:
                    self.screen.ids.player_grid.remove_widget(
                        player.main_layout)

                # shuffle list
                random.shuffle(self.current_players)
                # add players again
                for player in self.current_players:
                    self.screen.ids.player_grid.add_widget(player.main_layout)
                    player.main_layout.update_color(False)

                # order gamemode players in same order
                tmp = self.gamemode.players.copy()
                for i in range(len(tmp)):
                    self.gamemode.players[i] = self.get_player_from_list(
                        self.current_players[i].name, tmp)
            else:
                print("Shuffle works only of begin of game")
        else:
            print("no players")

    def get_player_widget_by_name(self, name):
        for player in self.current_players:
            if player.name == name:
                return player

    def restart_game(self):
        player_names = []
        for player in self.current_players:
            self.screen.ids.player_grid.remove_widget(player.main_layout)
            player_names.append(player.name)
        self.current_players.clear()

        self.gamemode = X01(self.gamemode.game_score)

        for name in player_names:
            player = PlayerWidget(name, self.gamemode.game_score)
            if len(self.current_players) == 0:
                player.main_layout.update_color(True)
            else:
                player.main_layout.update_color(False)
            self.current_players.append(player)
            self.screen.ids.player_grid.add_widget(player.main_layout)
            self.gamemode.add_player(name)

    def on_double_out_switched(self, checkbox, value):
        self.gamemode.double_out = value

    def menu_callback(self, text_item):
        self.gamemode.game_score = int(text_item)
        self.restart_game()
