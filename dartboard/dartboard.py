import numpy as np
import cv2
import math
import random


class Dartboard:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.radius = 0
        self.dartboard = None
        self.darboard_orignal = None
        self.img_center = (0, 0)
        self.radius_list = []
        self.borders = []

    # calculates circle middle and radius by 3 points
    def calculate_circle(self):
        x1 = self.p1[0]
        y1 = self.p1[1]

        x2 = self.p2[0]
        y2 = self.p2[1]

        x3 = self.p3[0]
        y3 = self.p3[1]

        x12 = x1 - x2
        x13 = x1 - x3
        y12 = y1 - y2
        y13 = y1 - y3
        y31 = y3 - y1
        y21 = y2 - y1
        x31 = x3 - x1
        x21 = x2 - x1

        # x1^2 - x3^2
        sx13 = pow(x1, 2) - pow(x3, 2)

        # y1^2 - y3^2
        sy13 = pow(y1, 2) - pow(y3, 2)
        sx21 = pow(x2, 2) - pow(x1, 2)
        sy21 = pow(y2, 2) - pow(y1, 2)

        f = ((sx13 * x12 + sy13 * x12 + sx21 * x13 + sy21 * x13) //
             (2 * (y31 * x12 - y21 * x13)))
        g = ((sx13 * y12 + sy13 * y12 + sx21 * y13 + sy21 * y13) //
             (2 * (x31 * y12 - x21 * y13)))
        c = (-pow(x1, 2) - pow(y1, 2) - 2 * g * x1 - 2 * f * y1)

        h = -g
        k = -f
        sqr_of_r = h * h + k * k - c

        # radius
        r = round(math.sqrt(sqr_of_r), 5)

        return h, k, r

    # returns point on circle by angle
    def get_point_by_angle(self, angle):
        x = self.img_center[0] + self.radius * \
            math.cos(angle * math.pi / 180.0)
        y = self.img_center[1] + self.radius * \
            math.sin(angle * math.pi / 180.0)
        return int(x), int(y)

    # check point in double or triple
    # return's multiplier name ("D" or "T") or ""
    def check_point_in_ring(self, point, outer_radius, inner_radius):
        if self.check_point_in_circle(point, outer_radius) and not self.check_point_in_circle(point, inner_radius):
            return True
        return False

    # check if point is inside triangle
    def check_point_in_triangle(self, p, p1, p2):
        dx = p[0] - p2[0]
        dy = p[1] - p2[1]
        dx21 = p2[0] - p1[0]
        dy12 = p1[1] - p2[1]
        d = dy12 * (self.img_center[0] - p2[0]) + \
            dx21 * (self.img_center[1] - p2[1])
        s = dy12 * dx + dx21 * dy
        t = (p2[1] - self.img_center[1]) * dx + \
            (self.img_center[0] - p2[0]) * dy
        if d < 0:
            return s <= 0 and t <= 0 and s + t >= d
        return s >= 0 and t >= 0 and s + t <= d

    # check if point is inside circle
    def check_point_in_circle(self, point, radius):
        radius_2 = radius ** 2
        value = (point[0] - self.img_center[0]) ** 2 + \
            (point[1] - self.img_center[1]) ** 2
        if value < radius_2:
            return True
        else:
            return False

    # checks what single point hit
    def check_point(self, point):
        # check inside bull or bulls eye
        circles = ["D25", "25", "-"]
        # check inside field
        numbers = ["20", "1", "18", "4", "13", "6", "10", "15", "2",
                   "17", "3", "19", "7", "16", "8", "11", "14", "9", "12", "5"]

        # check bulls eye, single bull, outside
        for i in range(3):
            if i == 2:
                if not self.check_point_in_circle(point, self.radius_list[i]):
                    return circles[i]
            elif self.check_point_in_circle(point, self.radius_list[i]):
                return circles[i]

        # check if inside normal field
        for x in range(20):
            if x == 19:
                if self.check_point_in_triangle(point, self.borders[x], self.borders[0]):
                    hit_value = ""
                    if self.check_point_in_ring(point, self.radius_list[2], self.radius_list[3]):
                        hit_value = "D"
                    if self.check_point_in_ring(point, self.radius_list[4], self.radius_list[5]):
                        hit_value = "T"
                    hit_value += numbers[x]
                    return hit_value
                return "-"

            if self.check_point_in_triangle(point, self.borders[x], self.borders[x + 1]):
                hit_value = ""
                if self.check_point_in_ring(point, self.radius_list[2], self.radius_list[3]):
                    hit_value = "D"
                if self.check_point_in_ring(point, self.radius_list[4], self.radius_list[5]):
                    hit_value = "T"
                hit_value += numbers[x]
                return hit_value

    # check list of points

    def test_points(self, dart_board, points):
        # draw test points
        for point in points:
            dart_board = cv2.circle(dart_board, point, 3, (0, 255, 0), -1)

        self.check_points(points)
        print("")
        return dart_board

    # draw full dartboard from 3 calibration points
    def draw_board(self):
        # radius
        x, y, self.radius = self.calculate_circle()
        radius_double_in_circle = int(self.radius * 0.953)
        radius_triple_out_circle = int(self.radius * 0.629)
        radius_triple_in_circle = int(self.radius * 0.582)
        radius_single_circle = int(self.radius * 0.187)
        radius_bull_circle = int(self.radius * 0.0747)
        radius = int(self.radius)
        self.radius_list = [radius_bull_circle, radius_single_circle, radius, radius_double_in_circle,
                            radius_triple_out_circle, radius_triple_in_circle]

        # create blank image
        img_size = radius * 2 + 30
        dart_board = np.zeros((img_size, img_size, 3), np.uint8)
        self.img_center = (int(img_size / 2), int(img_size / 2))
        offset_middle = (x - self.img_center[0], y - self.img_center[1])

        # draw circles
        for circle_radius in self.radius_list:
            dart_board = cv2.circle(
                dart_board, self.img_center, circle_radius, (128, 128, 128), 2)

        # draw boxes
        angle = -99  # -99 degree is for left line of twenty
        for i in range(20):
            new_point = self.get_point_by_angle(angle)
            dart_board = cv2.line(
                dart_board, (new_point[0], new_point[1]), self.img_center, (128, 128, 128), 2)
            self.borders.append(new_point)
            angle += 18

        # draw calibration points
        p1_offset = (self.p1[0] - offset_middle[0],
                     self.p1[1] - offset_middle[1])
        p2_offset = (self.p2[0] - offset_middle[0],
                     self.p2[1] - offset_middle[1])
        p3_offset = (self.p3[0] - offset_middle[0],
                     self.p3[1] - offset_middle[1])
        dart_board = cv2.circle(dart_board, p1_offset, 3, (0, 0, 255), -1)
        dart_board = cv2.circle(dart_board, p2_offset, 3, (0, 0, 255), -1)
        dart_board = cv2.circle(dart_board, p3_offset, 3, (0, 0, 255), -1)

        self.darboard_orignal = dart_board
        return dart_board

    def draw_point_on_board(self, point, reset):
        if reset:
            self.dartboard = self.darboard_orignal.copy()
        dartboard = cv2.circle(self.dartboard, point, 3, (0, 255, 0), -1)
        return dartboard

    # generate 3 random points in radius
    def get_random_point(self):
        random_x = random.randint(1, int(self.radius) * 2)
        random_y = random.randint(1, int(self.radius) * 2)
        point = (random_x, random_y)
        return point
