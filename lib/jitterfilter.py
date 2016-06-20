from .datacontainer import DataContainer

class AntiJitterFilter:
    @staticmethod
    def filter(datacontainer, value):
        value = int(value)
        datacontainer_frames_len = len(datacontainer.frames)
        if datacontainer_frames_len >= value * 2 + 1 and value > 0:
            datacontainer2 = DataContainer()
            datacontainer2.initial = datacontainer.initial
            for i, frame in enumerate(datacontainer.frames):
                if frame is not None and frame.points:
                    value2 = value if i >= value and i < datacontainer_frames_len - value else i if i < value else datacontainer_frames_len - i - 1
                    frame2 = datacontainer2.add_frame()
                    for j in range(len(frame.points)):
                        sum_x = 0
                        sum_y = 0
                        for k in range(value2 + 1):
                            previous_frame = datacontainer.frames[i - k] if datacontainer.frames[i - k] is not None and datacontainer.frames[i - k].points else frame
                            sum_x += previous_frame.points[j].x
                            sum_y += previous_frame.points[j].y
                            if k != 0:
                                next_frame = datacontainer.frames[i + k] if datacontainer.frames[i + k] is not None and datacontainer.frames[i + k].points else frame
                                sum_x += next_frame.points[j].x
                                sum_y += next_frame.points[j].y

                        frame2.add_point(sum_x / (value2 * 2 + 1), sum_y / (value2 * 2 + 1))

                else:
                    datacontainer2.frames.append(frame)

            return datacontainer2

        else:
            return datacontainer

