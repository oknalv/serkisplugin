class DataContainer:

    def __init__(self):
        self.frames = []
        self.fps = None
        self.initial = None

    def add_frame(self):
        frame = FrameContainer()
        self.frames.append(frame)
        return frame

    def add_initial(self):
        if not self.initial:
            self.initial = FrameContainer()

        return self.initial


class FrameContainer:

    def __init__(self):
        self.points = []

    def add_point(self, x, y):
        self.points.append(Point(x, y))


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
