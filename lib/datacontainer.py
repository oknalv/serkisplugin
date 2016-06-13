import math

class DataContainer:

    def __init__(self):
        self.frames = []
        self.fps = None
        self.initial = None
        self.pixel_proportion = None

    def add_frame(self):
        frame = FrameContainer()
        self.frames.append(frame)
        return frame

    def add_initial(self):
        if not self.initial:
            self.initial = FrameContainer()

        return self.initial

    """
    def get_pixel_proportion(self):
        #27 28
        if self.pixel_proportion is None:
            self.pixel_proportion = Point.get_distance(self.initial.points[27], self.initial.points[28])

        return self.pixel_proportion"""


class FrameContainer:

    def __init__(self):
        self.points = []

    def add_point(self, x, y):
        self.points.append(Point(x, y))


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def get_distance(p1, p2):
        return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

    @staticmethod
    def get_vertical_distance(p1, p2):
        return abs(p1.y - p2.y)

    @staticmethod
    def get_horizontal_distance(p1, p2):
        return abs(p1.x - p2.x)
