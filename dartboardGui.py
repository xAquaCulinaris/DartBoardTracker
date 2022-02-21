from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.boxlayout import BoxLayout

import os.path

from player_widget import PlayerWidget


Window.size = (1000, 600)

class DartboardGui(MDApp):
    #build inital screen
    def build(self):
        self.screen = Builder.load_file('main.kv')        
        self.player_names = []
        self.available_players_labes = []
        self.current_players = []
        self.load_player_names_from_file()
        
        return self.screen

    #get obj of a list of x.text objects
    def get_object_by_name(self, name, list):
        for obj in list:
            if obj.text == name:
                return obj
        return None

    #add player button pressed
    def add_player_pressed(self):
        # get name from textbox
        name = self.screen.ids.add_player_text.text
        # check that name is not empty and not already in currentplayer
        if not name == "" and self.get_player_from_list(name, self.current_players) == None:
            self.add_player_to_main_screen(name)
            #add player to current player menue
            mdButton = MDTextButton(text=name)
            mdButton.bind(on_press=self.remove_label_from_current)
            self.screen.ids.current_players_grid.add_widget(mdButton)

            #if player in available list remove it
            mdLabel = self.get_object_by_name(name, self.available_players_labes)
            if mdLabel:
                self.screen.ids.available_players_grid.remove_widget(mdLabel)
        
            #if name not already exists add name to file
            if not name in self.player_names:
                self.write_player_name_to_file(name)
            
        self.screen.ids.add_player_text.text = "" 

    def get_player_from_list(self, name, list):
        for player in list:
            if player.name == name:
                return player
        return None

    #writes a new player name to a file to save it permanently
    def write_player_name_to_file(self, name):
        # open file
        player_names_file = open('player_names.txt', 'a')
        #write name
        player_names_file.write(name+"\n")
        #close file
        player_names_file.close()
        #add name to list of all names
        self.player_names.append(name)
  
    #loads permanent players from file
    def load_player_names_from_file(self):
        if os.path.isfile('player_names.txt'):
            #open file
            player_names_file = open('player_names.txt', 'r')
            #get all lines
            names = player_names_file.readlines()
            #loop over each line
            for name in names:
                #add player name to list of players
                test = name.rstrip("\n")
                self.player_names.append(name.rstrip("\n"))
                #add label to available players 
                label = MDTextButton(text=name.rstrip("\n"))
                label.bind(on_press=self.remove_label_from_avilable)
                self.available_players_labes.append(label)
                self.screen.ids.available_players_grid.add_widget(label)
            player_names_file.close()

    #on button press removes label from list of available players
    def remove_label_from_avilable(self, button):
        self.screen.ids.available_players_grid.remove_widget(button)
        button.unbind(on_press=self.remove_label_from_avilable)
        button.bind(on_press=self.remove_label_from_current)
        self.screen.ids.current_players_grid.add_widget(button)
        #add player to main screen
        self.add_player_to_main_screen(button.text)


    #on button press remove label from list of current players
    def remove_label_from_current(self, button):
        #remove player from current players
        self.screen.ids.current_players_grid.remove_widget(button)
        #rebind button press
        button.unbind(on_press=self.remove_label_from_current)
        button.bind(on_press=self.remove_label_from_avilable)
        #add player to avaible palyers
        self.screen.ids.available_players_grid.add_widget(button)
        #remove player from main screen
        player = self.get_player_from_list(button.text, self.current_players)
        self.screen.ids.player_grid.remove_widget(player.main_layout)
        self.current_players.remove(player)
        
    def add_player_to_main_screen(self, name):
        player = PlayerWidget(name)
        self.current_players.append(player)
        self.screen.ids.player_grid.add_widget(player.main_layout)

