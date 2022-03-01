from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout

from gui.colorize_layout import CustomGraphics


class PlayerWidget:
    def __init__(self, player_name, start_value):
        # set playername
        self.name = player_name

        # create layouts
        self.main_layout = BoxLayout(
            orientation='vertical', size_hint=(None, None))
        self.points_layout = BoxLayout(orientation='horizontal')

        # create all labels
        self.point_labels = []
        name_label = MDLabel(text=self.name)
        name_label.bold = True
        name_label.font_size='18sp'

        self.total_score_label = MDLabel(text=str(start_value))
        self.total_score_label.font_size='20sp'
        self.current_score_label = MDLabel(text=str(0))
        self.avg_label = MDLabel(text="-")

        for i in range(3):
            label = MDLabel(text="0")
            self.point_labels.append(label)
            self.points_layout.add_widget(label)

        # add all to layouts
        self.main_layout.add_widget(name_label)
        self.main_layout.add_widget(self.total_score_label)
        self.main_layout.add_widget(self.points_layout)

        current_score_grid = BoxLayout(orientation='horizontal')
        current_score_grid.add_widget(self.current_score_label)
        current_score_grid.add_widget(self.avg_label)
        self.main_layout.add_widget(current_score_grid)
        # Color background of widget
        CustomGraphics.SetBG(self.main_layout, bg_color=[0.5, 0.5, 0.5])

    def update_score(self, player):
        index = player.get_current_index()

        self.point_labels[index].text = str(player.last_three_points[index])
        self.current_score_label.text = str(player.current_score)
        self.total_score_label.text = str(player.game_score)
        self.avg_label.text = str(player.get_avrg())
        
    def clear_score(self):
        for label in self.point_labels:
            label.text = "0"
        self.current_score_label.text = "0"  

