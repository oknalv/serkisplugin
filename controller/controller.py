from xml import sax as sax
import bpy
import math

from ..lib.datacontainer import DataContainer
from ..lib.keypointhandler import KeypointHandler


def generate(file, fps=None):
    dc = DataContainer()
    parser = sax.make_parser()
    parser.setContentHandler(KeypointHandler(dc))
    parser.parse(open(file, "rU"))
    if fps is None:
        fps = dc.fps

    bpy.context.scene.render.fps = fps

    prev = dc.initial
    move = []
    for ind, frame in enumerate(dc.frames):
        # TODO Move model: x,y in blender is x,z
        if frame.points:

            #desplazamiento vertical con respecto al previo
            desplv = frame.points[19].y - prev.points[19].y




            obj = bpy.data.objects["metarig"]
            hueso = obj.pose.bones["brow.T.R.001"]
            hueso.rotation_mode = "XYZ"
            hueso.rotation_euler.rotate_axis("X", frame.points[19].y - prev.points[19].y)
            obj.pose.bones["brow.T.R.001"].keyframe_insert('rotation_euler')
            bpy.context.scene.frame_current += 1
            # bpy.ops.transform.rotate(value=0.1, axis=(0, 1, 0)
            # obj.pose.bones["brow.T.R.001"].keyframe_insert('rotation_euler')
            # TODO Save position in frame

            for i, p in enumerate(prev.points):
                if is_moved(prev.points[i], frame.points[i]):
                    move.append(i)
                    prev.points[i] = frame.points[i]

        move = []


def is_moved(prev, actual):
    if prev.x != actual.x or prev.y != actual.y:
        return True
    return False