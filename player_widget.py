from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout

from color_widget import CustomGraphics


class PlayerWidget:
     def __init__(self, player_name):
        #set playername
        self.name = player_name

        #create layouts
        self.main_layout = BoxLayout(orientation='vertical', size_hint=(None, None))
        self.points_layout = BoxLayout(orientation='horizontal')

        #create all labels
        point_labels = []
        name_label = MDLabel(text=self.name)
        for i in range (3):
            label = MDLabel(text="0")
            point_labels.append(label)
            self.points_layout.add_widget(label)

       

        #add all to layouts
        self.main_layout.add_widget(name_label)
        self.main_layout.add_widget(self.points_layout)
        #Color background of widget
        CustomGraphics.SetBG(self.main_layout, bg_color=[0.5,0.5,0.5])

        
