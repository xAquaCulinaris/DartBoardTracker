from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout

class RoundedCornerBoxLayout(BoxLayout):
    def __init__(self, height = 200, width = 200):
        super().__init__(orientation='vertical', size_hint=(None, None))
        self.height = height
        self.width = width

    def update_color(self, status=True):
        color = None
        if status:
            color = 171/255
        else:
            color = 128/255

        with self.canvas.before:
            Color(color, color, color, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[(30, 30), (30, 30), (30, 30), (30, 30)],
            )
        self.bind(pos=lambda obj, pos: setattr(self.rect, "pos", pos))
        self.bind(size=lambda obj, size: setattr(self.rect, "size", size))
        