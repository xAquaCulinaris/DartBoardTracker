from kivymd.uix.label import MDLabel
from kivymd.uix.label import MDIcon
from kivymd.uix.boxlayout import BoxLayout

from gui.widgets.RoundedCornerBoxLayout import RoundedCornerBoxLayout


class PlayerWidget:
    def __init__(self, player_name, start_value):
        # set playername
        self.name = player_name

        # create layouts
        self.main_layout = RoundedCornerBoxLayout()
        self.points_layout = BoxLayout(orientation='horizontal')

        # create all labels
        self.point_labels = []
        name_label = MDLabel(text=self.name)
        name_label.bold = True
        name_label.font_size = '18sp'

        # total score
        self.total_score_label = MDLabel(text=str(start_value))
        self.total_score_label.font_size = '20sp'
        # total darts thrown
        # self.dart_icon = FitImage(source="assets/images/dart_icon.png")
        # self.dart_icon.size_hint_y = 1
        # self.dart_icon.icon_size ='16sp'

        self.current_score_label = MDLabel(text=str(0))
        self.avg_label = MDLabel(text="-")

        for i in range(3):
            label = MDLabel(text="0")
            self.point_labels.append(label)
            self.points_layout.add_widget(label)

        first_row_layout = BoxLayout(orientation='horizontal')
        first_row_layout.add_widget(self.total_score_label)
        # first_row_layout.add_widget(self.dart_icon)

        # add all to layouts
        self.main_layout.add_widget(name_label)
        self.main_layout.add_widget(first_row_layout)
        self.main_layout.add_widget(self.points_layout)

        current_score_grid = BoxLayout(orientation='horizontal')
        current_score_grid.add_widget(self.current_score_label)
        current_score_grid.add_widget(self.avg_label)
        self.main_layout.add_widget(current_score_grid)

        self.current_player_box = BoxLayout(orientation='horizontal')
        self.main_layout.add_widget(self.current_player_box)

        # Color background of widget
       # CustomGraphics.SetBG(self.main_layout, bg_color=[171/255, 171/255, 171/255])

    def update_score(self, player, over_throw):
        index = player.get_current_index()

        self.point_labels[index].text = str(player.last_three_points[index])
        if over_throw:
            self.point_labels[index].color = (1, 0, 0, 1)
            self.current_score_label.color = (1, 0, 0, 1)
        else:
            self.point_labels[index].color = (0, 0, 0, 1)
        self.current_score_label.text = str(player.current_score)
        self.total_score_label.text = str(player.game_score)
        self.avg_label.text = str(player.get_avrg())

        # remove current player indication
        if player.current_darts_thrown == 3:
            self.main_layout.update_color(False)

        
    def clear_score(self):
        for label in self.point_labels:
            label.text = ""
        self.current_score_label.color = (0, 0, 0, 1)
        self.current_score_label.text = "0"  

