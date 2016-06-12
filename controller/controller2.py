from xml import sax as sax
import bpy
import math

from ..lib.datacontainer import DataContainer
from ..lib.datacontainer import Point
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
        self.nose = armature.pose.bones["nose"]
        self.nose.rotation_mode = "XYZ"
        self.nostril_R = armature.pose.bones["nostril_R"]
        self.nostril_R.rotation_mode = "XYZ"
        self.nostril_L = armature.pose.bones["nostril_L"]
        self.nostril_L.rotation_mode = "XYZ"
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
        self.previous_points = None
        self.reference_point = 27

    def generate(self, file, fps=None):
        parser = sax.make_parser()
        parser.setContentHandler(KeypointHandler(self.data_container))
        parser.parse(open(file, "rU"))
        if fps is None:
            fps = self.data_container.fps

        bpy.context.scene.render.fps = fps
        previous_frame = self.data_container.initial
        # rotated_flag = False

        bpy.context.scene.frame_current = 0
        bpy.context.scene.frame_end = len(self.data_container.frames)

        for current_frame in self.data_container.frames:
            if current_frame.points:
                self.current_points = current_frame.points
                self.previous_points = previous_frame.points
                self.move_eyes()
                self.move_eyebrows()
                self.move_jaw()
                """
                ################# JAW #########################
                # 27 8 distance from nose to jaw
                jaw_current_aperture = Point.get_vertical_distance(self.current_points[27], self.current_points[8])
                jaw_previous_aperture = Point.get_vertical_distance(self.previous_points[27], self.previous_points[8])
                if jaw_current_aperture != jaw_previous_aperture:
                    jaw_aperture_difference = jaw_current_aperture - jaw_previous_aperture
                    self.jaw.rotation_euler.rotate_axis("X", jaw_aperture_difference / 100)
                    self.jaw.keyframe_insert("rotation_euler")

                ################# LIPS #########################
                # 60 27
                lips_right_side_current_horizontal_movement = Point.get_horizontal_distance(current_points[60], current_points[27])
                lips_right_side_previous_horizontal_movement = Point.get_horizontal_distance(previous_points[60], previous_points[27])
                lips_right_side_current_vertical_movement = Point.get_horizontal_distance(current_points[60], current_points[27])
                lips_right_side_previous_vertical_movement = Point.get_horizontal_distance(previous_points[60], previous_points[27])
                if lips_right_side_current_horizontal_movement != lips_right_side_previous_horizontal_movement:
                    lips_right_side_horizontal_aperture_difference = lips_right_side_current_horizontal_movement - lips_right_side_previous_horizontal_movement
                    lipside_R.rotation_euler.rotate_axis("Z", lips_right_side_horizontal_aperture_difference / 10)
                    rotated_flag = True

                if lips_right_side_current_vertical_movement != lips_right_side_previous_vertical_movement:
                    lips_right_side_vertical_aperture_difference = lips_right_side_current_vertical_movement - lips_right_side_previous_vertical_movement
                    lipside_R.rotation_euler.rotate_axis("X", lips_right_side_vertical_aperture_difference / 10)
                    rotated_flag = True

                if rotated_flag:
                    lipside_R.keyframe_insert("rotation_euler")
                    rotated_flag = False

                # 64 27
                lips_left_side_current_horizontal_movement = Point.get_horizontal_distance(current_points[64], current_points[27])
                lips_left_side_previous_horizontal_movement = Point.get_horizontal_distance(previous_points[64], previous_points[27])
                lips_left_side_current_vertical_movement = Point.get_horizontal_distance(current_points[64], current_points[27])
                lips_left_side_previous_vertical_movement = Point.get_horizontal_distance(previous_points[64], previous_points[27])
                if lips_left_side_current_horizontal_movement != lips_left_side_previous_horizontal_movement:
                    lips_left_side_horizontal_aperture_difference = lips_left_side_current_horizontal_movement - lips_left_side_previous_horizontal_movement
                    lipside_L.rotation_euler.rotate_axis("Z", lips_left_side_horizontal_aperture_difference / 10)
                    rotated_flag = True

                if lips_left_side_current_vertical_movement != lips_left_side_previous_vertical_movement:
                    lips_left_side_vertical_aperture_difference = lips_left_side_current_vertical_movement - lips_left_side_previous_vertical_movement
                    lipside_L.rotation_euler.rotate_axis("X", lips_left_side_vertical_aperture_difference / 10)
                    rotated_flag = True

                if rotated_flag:
                    lipside_L.keyframe_insert("rotation_euler")
                    rotated_flag = False

                # 62 27
                upper_lip_current_horizontal_movement = Point.get_horizontal_distance(current_points[62], current_points[27])
                upper_lip_previous_horizontal_movement = Point.get_horizontal_distance(previous_points[62], previous_points[27])
                upper_lip_current_vertical_movement = Point.get_horizontal_distance(current_points[62], current_points[27])
                upper_lip_previous_vertical_movement = Point.get_horizontal_distance(previous_points[62], previous_points[27])
                if upper_lip_current_horizontal_movement != upper_lip_previous_horizontal_movement:
                    upper_lip_horizontal_aperture_difference = upper_lip_current_horizontal_movement - upper_lip_previous_horizontal_movement
                    ulip.rotation_euler.rotate_axis("Z", upper_lip_horizontal_aperture_difference / 10)
                    rotated_flag = True

                if upper_lip_current_vertical_movement != upper_lip_previous_vertical_movement:
                    upper_lip_vertical_aperture_difference = upper_lip_current_vertical_movement - upper_lip_previous_vertical_movement
                    ulip.rotation_euler.rotate_axis("X", upper_lip_vertical_aperture_difference / 10)
                    rotated_flag = True

                if rotated_flag:
                    ulip.keyframe_insert("rotation_euler")
                    rotated_flag = False

                # 66 27
                lower_lip_current_horizontal_movement = Point.get_horizontal_distance(current_points[66], current_points[27])
                lower_lip_previous_horizontal_movement = Point.get_horizontal_distance(previous_points[66], previous_points[27])
                lower_lip_current_vertical_movement = Point.get_horizontal_distance(current_points[66], current_points[27])
                lower_lip_previous_vertical_movement = Point.get_horizontal_distance(previous_points[66], previous_points[27])
                if lower_lip_current_horizontal_movement != lower_lip_previous_horizontal_movement:
                    lower_lip_horizontal_aperture_difference = lower_lip_current_horizontal_movement - lower_lip_previous_horizontal_movement
                    dlip.rotation_euler.rotate_axis("Z", lower_lip_horizontal_aperture_difference / 10)
                    rotated_flag = True

                if lower_lip_current_vertical_movement != lower_lip_previous_vertical_movement:
                    lower_lip_vertical_aperture_difference = lower_lip_current_vertical_movement - lower_lip_previous_vertical_movement
                    dlip.rotation_euler.rotate_axis("X", lower_lip_vertical_aperture_difference / 10)
                    rotated_flag = True

                if rotated_flag:
                    dlip.keyframe_insert("rotation_euler")
                    rotated_flag = False

                ################# NOSE #########################
                # 34 27
                nose_current_rotation = Point.get_horizontal_distance(current_points[34], current_points[27])
                nose_previous_rotation = Point.get_horizontal_distance(previous_points[34], previous_points[27])
                if nose_current_rotation != nose_previous_rotation:
                    nose_rotation_difference = nose_current_rotation - nose_previous_rotation
                    nose.rotation_euler.rotate_axis("Z", nose_rotation_difference / 10)
                    nose.keyframe_insert("rotation_euler")

                # 31 35
                nostrils_current_distance = Point.get_horizontal_distance(current_points[31], current_points[21])
                nostrils_previous_distance = Point.get_horizontal_distance(previous_points[34], previous_points[27])
                if nostrils_current_distance != nostrils_previous_distance:
                    nostrils_distance_difference = nostrils_current_distance - nostrils_previous_distance
                    nostril_L.rotation_euler.rotate_axis("Y", nostrils_distance_difference / 20)
                    nostril_L.keyframe_insert("rotation_euler")
                    nostril_R.rotation_euler.rotate_axis("Y", - nostrils_distance_difference / 20)
                    nostril_R.keyframe_insert("rotation_euler")
                """

            bpy.context.scene.frame_current += 1
            previous_frame = current_frame

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
        self.move_single_eyebrow(22, 25, 26, self.eyebrow_L_001, self.eyebrow_L_002, self.eyebrow_L_003)

    def move_single_eyebrow(self, inner_eyebrow_point, middle_eyebrow_point,
                            outer_eyebrow_point, inner_eyebrow, middle_eyebrow, outer_eyebrow):
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
                   max(movement / initial_movement, negative_proportion_limit)) - negative_proportion_limit

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

