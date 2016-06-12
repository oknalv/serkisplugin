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
                """
                ################# JAW #########################
                # 27 8 distance from nose to jaw
                jaw_current_aperture = Point.get_vertical_distance(self.current_points[27], self.current_points[8])
                jaw_previous_aperture = Point.get_vertical_distance(self.previous_points[27], self.previous_points[8])
                if jaw_current_aperture != jaw_previous_aperture:
                    jaw_aperture_difference = jaw_current_aperture - jaw_previous_aperture
                    self.jaw.rotation_euler.rotate_axis("X", jaw_aperture_difference / 100)
                    self.jaw.keyframe_insert("rotation_euler")

                ################# RIGHT EYEBROW #########################
                # 21 27
                right_eyebrow_in_current_vertical_movement = Point.get_vertical_distance(current_points[21], current_points[27])
                right_eyebrow_in_previous_vertical_movement = Point.get_vertical_distance(previous_points[21], previous_points[27])
                right_eyebrow_in_current_horizontal_movement = Point.get_horizontal_distance(current_points[21], current_points[27])
                right_eyebrow_in_previous_horizontal_movement = Point.get_horizontal_distance(previous_points[21], previous_points[27])
                if right_eyebrow_in_current_vertical_movement != right_eyebrow_in_previous_vertical_movement:
                    right_eyebrow_in_vertical_movement_difference = right_eyebrow_in_current_vertical_movement - right_eyebrow_in_previous_vertical_movement
                    eyebrow_R_001.rotation_euler.rotate_axis("X", right_eyebrow_in_vertical_movement_difference / 100)
                    rotated_flag = True

                if right_eyebrow_in_current_horizontal_movement != right_eyebrow_in_previous_horizontal_movement:
                    right_eyebrow_in_horizontal_movement_difference = right_eyebrow_in_current_horizontal_movement - right_eyebrow_in_previous_horizontal_movement
                    eyebrow_R_001.rotation_euler.rotate_axis("Z", right_eyebrow_in_horizontal_movement_difference / 100)
                    rotated_flag = True

                if rotated_flag:
                    eyebrow_R_001.keyframe_insert("rotation_euler")
                    rotated_flag = False

                # 19 27
                right_eyebrow_middle_current_vertical_movement = Point.get_vertical_distance(current_points[19], current_points[27])
                right_eyebrow_middle_previous_vertical_movement = Point.get_vertical_distance(previous_points[19], previous_points[27])
                right_eyebrow_middle_current_horizontal_movement = Point.get_horizontal_distance(current_points[19], current_points[27])
                right_eyebrow_middle_previous_horizontal_movement = Point.get_horizontal_distance(previous_points[19], previous_points[27])
                if right_eyebrow_middle_current_vertical_movement != right_eyebrow_middle_previous_vertical_movement:
                    right_eyebrow_middle_vertical_movement_difference = right_eyebrow_middle_current_vertical_movement - right_eyebrow_middle_previous_vertical_movement
                    eyebrow_R_002.rotation_euler.rotate_axis("X", right_eyebrow_middle_vertical_movement_difference / 100)
                    rotated_flag = True

                if right_eyebrow_middle_current_horizontal_movement != right_eyebrow_middle_previous_horizontal_movement:
                    right_eyebrow_middle_horizontal_movement_difference = right_eyebrow_middle_current_horizontal_movement - right_eyebrow_middle_previous_horizontal_movement
                    eyebrow_R_002.rotation_euler.rotate_axis("Z", right_eyebrow_middle_horizontal_movement_difference / 100)
                    rotated_flag = True

                if rotated_flag:
                    eyebrow_R_002.keyframe_insert("rotation_euler")
                    rotated_flag = False

                # 17 27
                right_eyebrow_out_current_vertical_movement = Point.get_vertical_distance(current_points[17], current_points[27])
                right_eyebrow_out_previous_vertical_movement = Point.get_vertical_distance(previous_points[17], previous_points[27])
                right_eyebrow_out_current_horizontal_movement = Point.get_horizontal_distance(current_points[17], current_points[27])
                right_eyebrow_out_previous_horizontal_movement = Point.get_horizontal_distance(previous_points[17], previous_points[27])
                if right_eyebrow_out_current_vertical_movement != right_eyebrow_out_previous_vertical_movement:
                    right_eyebrow_out_vertical_movement_difference = right_eyebrow_out_current_vertical_movement - right_eyebrow_out_previous_vertical_movement
                    eyebrow_R_003.rotation_euler.rotate_axis("X", right_eyebrow_out_vertical_movement_difference / 100)
                    rotated_flag = True

                if right_eyebrow_out_current_horizontal_movement != right_eyebrow_out_previous_horizontal_movement:
                    right_eyebrow_out_horizontal_movement_difference = right_eyebrow_out_current_horizontal_movement - right_eyebrow_out_previous_horizontal_movement
                    eyebrow_R_003.rotation_euler.rotate_axis("Z", right_eyebrow_out_horizontal_movement_difference / 100)
                    rotated_flag = True

                if rotated_flag:
                    eyebrow_R_003.keyframe_insert("rotation_euler")
                    rotated_flag = False

                ################# LEFT EYEBROW #########################
                # 22 27
                left_eyebrow_in_current_vertical_movement = Point.get_vertical_distance(current_points[22], current_points[27])
                left_eyebrow_in_previous_vertical_movement = Point.get_vertical_distance(previous_points[22], previous_points[27])
                left_eyebrow_in_current_horizontal_movement = Point.get_horizontal_distance(current_points[22], current_points[27])
                left_eyebrow_in_previous_horizontal_movement = Point.get_horizontal_distance(previous_points[22], previous_points[27])
                if left_eyebrow_in_current_vertical_movement != left_eyebrow_in_previous_vertical_movement:
                    left_eyebrow_in_vertical_movement_difference = left_eyebrow_in_current_vertical_movement - left_eyebrow_in_previous_vertical_movement
                    eyebrow_L_001.rotation_euler.rotate_axis("X", left_eyebrow_in_vertical_movement_difference / 100)
                    rotated_flag = True

                if left_eyebrow_in_current_horizontal_movement != left_eyebrow_in_previous_horizontal_movement:
                    left_eyebrow_in_horizontal_movement_difference = left_eyebrow_in_current_horizontal_movement - left_eyebrow_in_previous_horizontal_movement
                    eyebrow_L_001.rotation_euler.rotate_axis("Z", left_eyebrow_in_horizontal_movement_difference / 100)
                    rotated_flag = True

                if rotated_flag:
                    eyebrow_L_001.keyframe_insert("rotation_euler")
                    rotated_flag = False

                # 24 27
                left_eyebrow_middle_current_vertical_movement = Point.get_vertical_distance(current_points[24], current_points[27])
                left_eyebrow_middle_previous_vertical_movement = Point.get_vertical_distance(previous_points[24], previous_points[27])
                left_eyebrow_middle_current_horizontal_movement = Point.get_horizontal_distance(current_points[24], current_points[27])
                left_eyebrow_middle_previous_horizontal_movement = Point.get_horizontal_distance(previous_points[24], previous_points[27])
                if left_eyebrow_middle_current_vertical_movement != left_eyebrow_middle_previous_vertical_movement:
                    left_eyebrow_middle_vertical_movement_difference = left_eyebrow_middle_current_vertical_movement - left_eyebrow_middle_previous_vertical_movement
                    eyebrow_L_002.rotation_euler.rotate_axis("X", left_eyebrow_middle_vertical_movement_difference / 100)
                    rotated_flag = True

                if left_eyebrow_middle_current_horizontal_movement != left_eyebrow_middle_previous_horizontal_movement:
                    left_eyebrow_middle_horizontal_movement_difference = left_eyebrow_middle_current_horizontal_movement - left_eyebrow_middle_previous_horizontal_movement
                    eyebrow_L_002.rotation_euler.rotate_axis("Z", left_eyebrow_middle_horizontal_movement_difference / 100)
                    rotated_flag = True

                if rotated_flag:
                    eyebrow_L_002.keyframe_insert("rotation_euler")
                    rotated_flag = False

                # 26 27
                left_eyebrow_out_current_vertical_movement = Point.get_vertical_distance(current_points[26], current_points[27])
                left_eyebrow_out_previous_vertical_movement = Point.get_vertical_distance(previous_points[26], previous_points[27])
                left_eyebrow_out_current_horizontal_movement = Point.get_horizontal_distance(current_points[26], current_points[27])
                left_eyebrow_out_previous_horizontal_movement = Point.get_horizontal_distance(previous_points[26], previous_points[27])
                if left_eyebrow_out_current_vertical_movement != left_eyebrow_out_previous_vertical_movement:
                    left_eyebrow_out_vertical_movement_difference = left_eyebrow_out_current_vertical_movement - left_eyebrow_out_previous_vertical_movement
                    eyebrow_L_003.rotation_euler.rotate_axis("X", left_eyebrow_out_vertical_movement_difference / 100)
                    rotated_flag = True

                if left_eyebrow_out_current_horizontal_movement != left_eyebrow_out_previous_horizontal_movement:
                    left_eyebrow_out_horizontal_movement_difference = left_eyebrow_out_current_horizontal_movement - left_eyebrow_out_previous_horizontal_movement
                    eyebrow_L_003.rotation_euler.rotate_axis("Z", left_eyebrow_out_horizontal_movement_difference / 100)
                    rotated_flag = True

                if rotated_flag:
                    eyebrow_L_003.keyframe_insert("rotation_euler")
                    rotated_flag = False

                previous_frame = current_frame

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

    def move_eyes(self):
        # right eye, points 37 and 41
        self.move_single_eye(37, 41, self.ueyelid_R, self.deyelid_R)
        # left eye, points 44 and 46
        self.move_single_eye(44, 46, self.ueyelid_L, self.deyelid_L)

    def move_single_eye(self, upper_eyelid_point, lower_eyelid_point, upper_eyelid, lower_eyelid):
        aperture = Point.get_distance(
            self.current_points[upper_eyelid_point],
            self.current_points[lower_eyelid_point])
        upper_eyelid.rotation_euler.zero()
        lower_eyelid.rotation_euler.zero()
        original_aperture = Point.get_distance(
            self.data_container.initial.points[upper_eyelid_point],
            self.data_container.initial.points[lower_eyelid_point])
        upper_eyelid_end = -10
        upper_eyelid_start = 30
        lower_eyelid_end = 10
        lower_eyelid_start = 0
        full_open_proportion = 1.25
        full_close_proportion = 0.25
        aperture_proportion = min(full_open_proportion, max(aperture / original_aperture, full_close_proportion)) - full_close_proportion
        upper_eyelid_direction = -1 if upper_eyelid_end < upper_eyelid_start else 1
        lower_eyelid_direction = -1 if lower_eyelid_end < lower_eyelid_start else 1
        upper_eyelid_rotation_angles = (abs(upper_eyelid_start - upper_eyelid_end)) * aperture_proportion * upper_eyelid_direction / (abs(full_open_proportion - full_close_proportion))
        upper_eyelid.rotation_euler.rotate_axis(
            "X",
            math.radians(upper_eyelid_start))
        upper_eyelid.rotation_euler.rotate_axis(
            "X",
            math.radians(upper_eyelid_rotation_angles))
        print(abs(lower_eyelid_start - lower_eyelid_end))
        lower_eyelid_rotation_angles = (abs(lower_eyelid_start - lower_eyelid_end)) * aperture_proportion * lower_eyelid_direction / (abs(full_open_proportion - full_close_proportion))
        lower_eyelid.rotation_euler.rotate_axis(
            "X",
            math.radians(lower_eyelid_start))
        lower_eyelid.rotation_euler.rotate_axis(
            "X",
            math.radians(lower_eyelid_rotation_angles))
        upper_eyelid.keyframe_insert("rotation_euler")
        lower_eyelid.keyframe_insert("rotation_euler")

