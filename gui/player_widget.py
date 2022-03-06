from kivymd.uix.label import MDLabel
from kivymd.uix.label import MDIcon
from kivymd.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from gui.widgets.RoundedCornerBoxLayout import RoundedCornerBoxLayout


class PlayerWidget:
    def __init__(self, player_name, start_value):
        # set playername
        self.name = player_name

        # create layouts
        self.main_layout = RoundedCornerBoxLayout()
        self.points_layout = BoxLayout(orientation='horizontal')

        # name lables
        name_label = MDLabel(text=self.name)
        name_label.bold = True
        name_label.font_size = '28sp'
        name_label.pos_hint = {'x': 0.25, 'y': 0.0}

        # total score
        self.total_score_label = MDLabel(text=str(start_value))
        self.total_score_label.bold = True
        self.total_score_label.font_size = '26sp'
        self.total_score_label.padding_x = 10

        # total darts thrown
        self.dart_icon = MDIcon(icon="assets/images/dart_icon.png")
        self.dart_icon.size_hint = (0.5, 0.9)
        self.total_darts_thrown_label = MDLabel(text=str(0))
        self.total_darts_thrown_label.font_size = '24sp'  

        self.toal_darts_layout = BoxLayout(orientation="horizontal")
        self.toal_darts_layout.add_widget(self.dart_icon)
        self.toal_darts_layout.add_widget(self.total_darts_thrown_label)


        # current socre label
        self.current_score_label = MDLabel(text=str(0))
        self.current_score_label.font_size = '24sp'
        self.current_score_label.padding_x = 10



        # avg label
        self.avrg_icon = MDIcon(icon="assets/images/avrg_icon.png")
        self.avrg_icon.size_hint = (0.3, 0.6)
        self.avg_label = MDLabel(text="-")
        self.avg_label.font_size = '24sp'
        

        self.avrg_layout = BoxLayout(orientation="horizontal")
        self.avrg_layout.add_widget(self.avrg_icon)
        self.avrg_layout.add_widget(self.avg_label)

        
        #points lables
        self.point_labels = []
        for i in range(3):
            label = MDLabel(text="0")
            label.font_size = '24sp'
            if i == 0:
                label.padding_x = 10
            self.point_labels.append(label)
            self.points_layout.add_widget(label)

        first_row_layout = BoxLayout(orientation='horizontal')
        first_row_layout.add_widget(self.total_score_label)
        first_row_layout.add_widget(self.toal_darts_layout)

        # add all to layouts
        self.main_layout.add_widget(name_label)
        self.main_layout.add_widget(first_row_layout)
        self.main_layout.add_widget(self.points_layout)

        current_score_grid = BoxLayout(orientation='horizontal')
        current_score_grid.add_widget(self.current_score_label)
        current_score_grid.add_widget(self.avrg_layout)
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
        self.total_darts_thrown_label.text = str(player.total_darts_thrown)

        # remove current player indication
        if player.current_darts_thrown == 3:
            self.main_layout.update_color(False)

    def clear_score(self):
        for label in self.point_labels:
            label.text = ""
        self.current_score_label.color = (0, 0, 0, 1)
        self.current_score_label.text = "0"
