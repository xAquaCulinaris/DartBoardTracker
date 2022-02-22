#main.py
from dartboard.dartboard import Dartboard
from gui.dartboardGui import DartboardGui


#calibration points
point1 = (650, 435)  # 650, 435    3
point2 = (754, 1050)  # 754, 1050   20
point3 = (1032, 660)  # 1032, 660   6

#create dartboard from points
dartboard = Dartboard(point1, point2, point3)
dartboard_img = dartboard.draw_board()

#draw gui
dartboard_gui = DartboardGui()
dartboard_gui.dartboard = dartboard
dartboard_gui.run()