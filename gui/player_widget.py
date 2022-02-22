from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout

from gui.colorize_layout import CustomGraphics


class PlayerWidget:
    def __init__(self, player_name):
        # set playername
        self.total_score = 501
        self.current_score = 0
        self.name = player_name
        self.total_darts_thrown = 0
        self.current_darts_thrown = 0

        # create layouts
        self.main_layout = BoxLayout(
            orientation='vertical', size_hint=(None, None))
        self.points_layout = BoxLayout(orientation='horizontal')

        # create all labels
        self.point_labels = []
        name_label = MDLabel(text=self.name)
        self.total_score_label = MDLabel(text=str(self.total_score))
        self.current_score_label = MDLabel(text=str(self.current_score))

        for i in range(3):
            label = MDLabel(text="0")
            self.point_labels.append(label)
            self.points_layout.add_widget(label)

        # add all to layouts
        self.main_layout.add_widget(name_label)
        self.main_layout.add_widget(self.total_score_label)
        self.main_layout.add_widget(self.points_layout)
        self.main_layout.add_widget(self.current_score_label)
        # Color background of widget
        CustomGraphics.SetBG(self.main_layout, bg_color=[0.5, 0.5, 0.5])

    def update_score(self, score):
        self.point_labels[self.current_darts_thrown].text = str(score)
        score_number = self.score_string_to_number(score)
        self.current_score += score_number
        self.total_score -= score_number
        self.current_score_label.text = str(self.current_score)
        self.total_score_label.text = str(self.total_score)
        
        if self.current_darts_thrown == 2:
            self.current_darts_thrown = 0
            self.current_score = 0
        else:
            self.current_darts_thrown += 1

        return self.current_darts_thrown

    def score_string_to_number(self, score):
        s0 = score[0]
        if s0 == '-':
            return 0
        if s0 == 'D':
            return 2*int(score[1:])
        if s0 == 'T':
            return 3*int(score[1:])
        return int(score)
        

