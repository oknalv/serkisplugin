from xml import sax as sax

from ..lib.datacontainer import DataContainer
from ..lib.keypointhandler import KeypointHandler


def generate(self, file, fps=None):
    dc = DataContainer()
    parser = sax.make_parser()
    parser.setContentHandler(KeypointHandler(dc))
    parser.parse(open(file, "rU"))
    if fps is not None:
        dc.fps = fps
    print(dc.fps)