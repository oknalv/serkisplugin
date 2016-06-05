from xml import sax as sax
import bpy

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

