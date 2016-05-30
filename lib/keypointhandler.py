from xml.sax import ContentHandler


class KeypointHandler(ContentHandler):

    def __init__(self, datacontainer):
        self.datacontainer = datacontainer
        self.is_initial = False
        self.current_frame = None

    def startElement(self, name, attrs):
        if name == "fps":
            self.datacontainer.fps = float(attrs.getValue("value"))

        elif name == "initial":
            self.is_initial = True

        elif name == "img":
            if self.is_initial:
                self.current_frame = self.datacontainer.add_initial()

            else:
                self.current_frame = self.datacontainer.add_frame()

        elif name == "point":
            self.current_frame.add_point(attrs.getValue("x"), attrs.getValue("y"))

    def endElement(self, name):
        if name == "initial":
            self.is_initial = False
