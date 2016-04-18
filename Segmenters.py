from Image import Image


#######################################################################################################################
class Segmenter:
    def __init__(self):
        pass

    def get_current_segment(self):
        pass

    def get_next_segment(self):
        pass

    def has_next_segment(self):
        pass

    def reset_trajectory(self):
        pass


#######################################################################################################################
class RectangularSegmenter(Segmenter):
    # --------------------------------------------------------------------------
    def __init__(self, PILImage, heightRectangle, widthRectangle, trajectory, lstPreprocessing=[]):

        self.image = PILImage
        self.height = heightRectangle
        self.width = widthRectangle
        self.trajectory = trajectory
        self.lstPreprocessing = lstPreprocessing

    def reset_trajectory(self):
        self.trajectory.reset_position()

    def has_next_segment(self):
        return self.trajectory.has_next_position()

    # --------------------------------------------------------------------------
    def get_current_segment(self):

        centerCorner = self.trajectory.get_position()
        upperLeftCorner = [centerCorner[0], centerCorner[1]]
        upperLeftCorner[0] = centerCorner[0] - (self.width / 2)
        upperLeftCorner[1] = centerCorner[1] - (self.height / 2)
        lowerRightCorner = [centerCorner[0], centerCorner[1]]
        lowerRightCorner[0] += (self.width / 2)
        lowerRightCorner[1] += (self.height / 2)

        cutout = self.image.crop((upperLeftCorner[0], upperLeftCorner[1], lowerRightCorner[0], lowerRightCorner[1]))

        for processing in self.lstPreprocessing:
            cutout = processing.process(cutout)

        return Image(centerCorner[0], centerCorner[1], cutout)

    # --------------------------------------------------------------------------
    def get_next_segment(self):

        if (not self.has_next_segment()):
            return None

        centerCorner = self.trajectory.get_next_position()
        upperLeftCorner = [centerCorner[0], centerCorner[1]]
        upperLeftCorner[0] = centerCorner[0] - (self.width / 2)
        upperLeftCorner[1] = centerCorner[1] - (self.height / 2)
        lowerRightCorner = [centerCorner[0], centerCorner[1]]
        lowerRightCorner[0] += (self.width / 2)
        lowerRightCorner[1] += (self.height / 2)

        cutout = self.image.crop((upperLeftCorner[0], upperLeftCorner[1], lowerRightCorner[0], lowerRightCorner[1]))

        for processing in self.lstPreprocessing:
            cutout = processing.process(cutout)

        return Image(centerCorner[0], centerCorner[1], cutout)

#######################################################################################################################
