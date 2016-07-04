from xml import sax as sax
import bpy
import math

from ..lib.datacontainer import DataContainer
from ..lib.datacontainer import Point
from ..lib.jitterfilter import AntiJitterFilter
from ..lib.keypointhandler import KeypointHandler


class Controller:
    def __init__(self):
        armature = bpy.data.objects["Armature"]
        self.ueyelid_R = armature.pose.bones["ueyelid_R"]
        self.ueyelid_R.rotation_mode = "XYZ"
        self.ueyelid_L = armature.pose.bones["ueyelid_L"]
        self.ueyelid_L.rotation_mode = "XYZ"
        self.deyelid_R = armature.pose.bones["deyelid_R"]
        self.deyelid_R.rotation_mode = "XYZ"
        self.deyelid_L = armature.pose.bones["deyelid_L"]
        self.deyelid_L.rotation_mode = "XYZ"
        self.jaw = armature.pose.bones["jaw"]
        self.jaw.rotation_mode = "XYZ"
        self.eyebrow_L_001 = armature.pose.bones["eyebrow_L.001"]
        self.eyebrow_L_001.rotation_mode = "XYZ"
        self.eyebrow_L_002 = armature.pose.bones["eyebrow_L.002"]
        self.eyebrow_L_002.rotation_mode = "XYZ"
        self.eyebrow_L_003 = armature.pose.bones["eyebrow_L.003"]
        self.eyebrow_L_003.rotation_mode = "XYZ"
        self.eyebrow_R_001 = armature.pose.bones["eyebrow_R.001"]
        self.eyebrow_R_001.rotation_mode = "XYZ"
        self.eyebrow_R_002 = armature.pose.bones["eyebrow_R.002"]
        self.eyebrow_R_002.rotation_mode = "XYZ"
        self.eyebrow_R_003 = armature.pose.bones["eyebrow_R.003"]
        self.eyebrow_R_003.rotation_mode = "XYZ"
        self.lipside_R = armature.pose.bones["lipside_R"]
        self.lipside_R.rotation_mode = "XYZ"
        self.lipside_L = armature.pose.bones["lipside_L"]
        self.lipside_L.rotation_mode = "XYZ"
        self.ulip = armature.pose.bones["ulip"]
        self.ulip.rotation_mode = "XYZ"
        self.dlip = armature.pose.bones["dlip"]
        self.dlip.rotation_mode = "XYZ"
        self.data_container = DataContainer()
        self.current_points = None
        self.reference_point = 27

    def generate(self, file, jitter=0, fps=None):
        parser = sax.make_parser()
        parser.setContentHandler(KeypointHandler(self.data_container))
        parser.parse(open(file, "rU"))
        if fps is None:
            fps = self.data_container.fps

        bpy.context.scene.render.fps = fps
        bpy.context.scene.frame_current = 0
        bpy.context.scene.frame_end = len(self.data_container.frames)
        self.data_container = AntiJitterFilter.filter(self.data_container, jitter)
        for i, current_frame in enumerate(self.data_container.frames):
            if current_frame.points:
                self.current_points = current_frame.points
                self.move_eyes()
                self.move_eyebrows()
                self.move_jaw()
                self.move_lips()

            bpy.context.scene.frame_current += 1

    def move_lips(self):
        # upper and lower lip, points 62 and 66
        self.ulip.rotation_euler.zero()
        self.dlip.rotation_euler.zero()
        upper_lip_end_limit = -7
        upper_lip_start_limit = 5
        lower_lip_end_limit = 20
        lower_lip_start_limit = 0
        upper_lip_point = 62
        lower_lip_point = 66
        aperture = Point.get_distance(
            self.current_points[upper_lip_point],
            self.current_points[lower_lip_point])
        original_aperture = Point.get_distance(
            self.data_container.initial.points[upper_lip_point],
            self.data_container.initial.points[lower_lip_point])
        upper_lip_rotation_angles = self.get_rotation_angles(upper_lip_end_limit, upper_lip_start_limit, aperture,
                                                             original_aperture)
        lower_lip_rotation_angles = self.get_rotation_angles(lower_lip_end_limit, lower_lip_start_limit, aperture,
                                                             original_aperture)
        self.ulip.rotation_euler.rotate_axis("X", math.radians(upper_lip_start_limit))
        self.ulip.rotation_euler.rotate_axis("X", math.radians(upper_lip_rotation_angles))
        self.dlip.rotation_euler.rotate_axis("X", math.radians(lower_lip_start_limit))
        self.dlip.rotation_euler.rotate_axis("X", math.radians(lower_lip_rotation_angles))
        self.ulip.keyframe_insert("rotation_euler")
        self.dlip.keyframe_insert("rotation_euler")
        # lip sides, points 60 and 64
        self.lipside_R.rotation_euler.zero()
        self.lipside_L.rotation_euler.zero()
        right_side_lip_point = 60
        left_side_lip_point = 64
        right_side_lip_horizontal_end_limit = 10
        right_side_lip_horizontal_start_limit = -10
        left_side_lip_horizontal_end_limit = - right_side_lip_horizontal_end_limit
        left_side_lip_horizontal_start_limit = - right_side_lip_horizontal_start_limit
        self.move_single_point(right_side_lip_point, self.lipside_R, right_side_lip_horizontal_start_limit,
                               right_side_lip_horizontal_end_limit, "Z")
        self.move_single_point(left_side_lip_point, self.lipside_L, left_side_lip_horizontal_start_limit,
                               left_side_lip_horizontal_end_limit, "Z")
        side_lip_vertical_end_limit = -10
        side_lip_vertical_start_limit = 10
        self.move_single_point(right_side_lip_point, self.lipside_R, side_lip_vertical_start_limit,
                               side_lip_vertical_end_limit, "X")
        self.move_single_point(left_side_lip_point, self.lipside_L, side_lip_vertical_start_limit,
                               side_lip_vertical_end_limit, "X")
        self.lipside_R.keyframe_insert("rotation_euler")
        self.lipside_L.keyframe_insert("rotation_euler")



    def move_jaw(self):
        # point 8
        self.jaw.rotation_euler.zero()
        jaw_end_limit = 10
        jaw_start_limit = 0
        self.move_single_point(8, self.jaw, jaw_start_limit, jaw_end_limit, "X", multiplier=10)
        self.jaw.keyframe_insert("rotation_euler")

    def move_eyebrows(self):
        # right eyebrow, points 17, 19 and 21
        self.move_single_eyebrow(21, 19, 17, self.eyebrow_R_001, self.eyebrow_R_002, self.eyebrow_R_003)
        # left eyebrow, points 22, 25 and 26
        self.move_single_eyebrow(22, 25, 26, self.eyebrow_L_001, self.eyebrow_L_002, self.eyebrow_L_003, mirror=True)

    def move_single_eyebrow(self, inner_eyebrow_point, middle_eyebrow_point,
                            outer_eyebrow_point, inner_eyebrow, middle_eyebrow, outer_eyebrow, mirror=False):
        inner_eyebrow.rotation_euler.zero()
        middle_eyebrow.rotation_euler.zero()
        outer_eyebrow.rotation_euler.zero()
        inner_eyebrow_vertical_end_limit = -4
        inner_eyebrow_vertical_start_limit = 2
        middle_eyebrow_vertical_end_limit = 4
        middle_eyebrow_vertical_start_limit = -5
        outer_eyebrow_vertical_end_limit = 4
        outer_eyebrow_vertical_start_limit = -2
        self.move_single_point(inner_eyebrow_point, inner_eyebrow,
                               inner_eyebrow_vertical_start_limit, inner_eyebrow_vertical_end_limit, "X")
        self.move_single_point(middle_eyebrow_point, middle_eyebrow,
                               middle_eyebrow_vertical_start_limit, middle_eyebrow_vertical_end_limit, "X")
        self.move_single_point(outer_eyebrow_point, outer_eyebrow,
                               outer_eyebrow_vertical_start_limit, outer_eyebrow_vertical_end_limit, "X")
        inner_eyebrow_horizontal_end_limit = 0
        inner_eyebrow_horizontal_start_limit = -1
        middle_eyebrow_horizontal_end_limit = -1
        middle_eyebrow_horizontal_start_limit = 2
        outer_eyebrow_horizontal_end_limit = -1
        outer_eyebrow_horizontal_start_limit = 1
        if mirror:
            inner_eyebrow_horizontal_end_limit *= -1
            inner_eyebrow_horizontal_start_limit *= -1
            middle_eyebrow_horizontal_end_limit *= -1
            middle_eyebrow_horizontal_start_limit *= -1
            outer_eyebrow_horizontal_end_limit *= -1
            outer_eyebrow_horizontal_start_limit *= -1

        self.move_single_point(inner_eyebrow_point, inner_eyebrow,
                               inner_eyebrow_horizontal_start_limit, inner_eyebrow_horizontal_end_limit, "Z")
        self.move_single_point(middle_eyebrow_point, middle_eyebrow,
                               middle_eyebrow_horizontal_start_limit, middle_eyebrow_horizontal_end_limit, "Z")
        self.move_single_point(outer_eyebrow_point, outer_eyebrow,
                               outer_eyebrow_horizontal_start_limit, outer_eyebrow_horizontal_end_limit, "Z")
        inner_eyebrow.keyframe_insert("rotation_euler")
        middle_eyebrow.keyframe_insert("rotation_euler")
        outer_eyebrow.keyframe_insert("rotation_euler")

    def move_single_point(self, point, bone, start_limit, end_limit, axis, multiplier=1):
        current_distance = Point.get_vertical_distance(
            self.current_points[self.reference_point],
            self.current_points[point]) if axis == "X" else Point.get_horizontal_distance(
            self.current_points[self.reference_point],
            self.current_points[point])
        initial_distance = Point.get_vertical_distance(
            self.data_container.initial.points[self.reference_point],
            self.data_container.initial.points[point]) if axis == "X" else Point.get_horizontal_distance(
            self.data_container.initial.points[self.reference_point],
            self.data_container.initial.points[point])
        movement_angles = self.get_rotation_angles(end_limit, start_limit, current_distance, initial_distance)
        bone.rotation_euler.rotate_axis(axis, math.radians(start_limit))
        bone.rotation_euler.rotate_axis(axis, math.radians(movement_angles * multiplier))

    def move_eyes(self):
        # right eye, points 37 and 41
        self.move_single_eye(37, 41, self.ueyelid_R, self.deyelid_R)
        # left eye, points 44 and 46
        self.move_single_eye(44, 46, self.ueyelid_L, self.deyelid_L)

    def move_single_eye(self, upper_eyelid_point, lower_eyelid_point, upper_eyelid, lower_eyelid):
        aperture = Point.get_distance(
            self.current_points[upper_eyelid_point],
            self.current_points[lower_eyelid_point])
        original_aperture = Point.get_distance(
            self.data_container.initial.points[upper_eyelid_point],
            self.data_container.initial.points[lower_eyelid_point])
        upper_eyelid_end = -10
        upper_eyelid_start = 30
        lower_eyelid_end = 10
        lower_eyelid_start = 0
        upper_eyelid.rotation_euler.zero()
        lower_eyelid.rotation_euler.zero()
        upper_eyelid_rotation_angles = self.get_rotation_angles(upper_eyelid_end, upper_eyelid_start, aperture,
                                                                original_aperture)
        upper_eyelid.rotation_euler.rotate_axis("X", math.radians(upper_eyelid_start))
        upper_eyelid.rotation_euler.rotate_axis("X", math.radians(upper_eyelid_rotation_angles))
        lower_eyelid_rotation_angles = self.get_rotation_angles(lower_eyelid_end, lower_eyelid_start, aperture,
                                                                original_aperture)
        lower_eyelid.rotation_euler.rotate_axis("X", math.radians(lower_eyelid_start))
        lower_eyelid.rotation_euler.rotate_axis("X", math.radians(lower_eyelid_rotation_angles))
        upper_eyelid.keyframe_insert("rotation_euler")
        lower_eyelid.keyframe_insert("rotation_euler")

    def get_movement_proportion(self, movement, initial_movement, negative_proportion_limit, positive_proportion_limit):
        return min(positive_proportion_limit,
                   max(movement / initial_movement if initial_movement != 0 else 0.0000001,
                       negative_proportion_limit)) - negative_proportion_limit

    def get_proportional_limits(self, start_limit, end_limit):
        positive_proportion_limit = 1 + (end_limit / (end_limit - start_limit))
        negative_proportion_limit = 1 + (start_limit / (end_limit - start_limit))
        return positive_proportion_limit, negative_proportion_limit

    def get_rotation_angles(self, end_limit, start_limit, movement, initial_movement):
        direction = self.get_direction(end_limit, start_limit)
        positive_proportion_limit, negative_proportion_limit = self.get_proportional_limits(start_limit, end_limit)
        movement_proportion = self.get_movement_proportion(movement, initial_movement,
                                                           negative_proportion_limit, positive_proportion_limit)
        return (abs(start_limit - end_limit)) * movement_proportion * direction / (
        abs(positive_proportion_limit - negative_proportion_limit))

    def get_direction(self, end, start):
        return -1 if end < start else 1

