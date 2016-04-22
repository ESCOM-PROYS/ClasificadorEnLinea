#######################################################################################################################
from numpy.core.defchararray import center


class Trajectory:

    def __init__(self):
        pass

    def get_next_position(self):
        pass

    def get_position(self):
        pass

    def has_next_position(self):
        pass

    def reset_position(self):
        pass


#######################################################################################################################

class SimpleTrajectory(Trajectory):
    def __init__(self, horizontal_stride, vertical_stride, top_offset, left_offset, rigth_offset, bottom_offset,
                 width_image, height_image):

        Trajectory.__init__(self)

        self.top_offset = float(top_offset)
        self.left_offset = float(left_offset)
        self.right_offset = float(rigth_offset)
        self.bottom_offset = float(bottom_offset)
        self.horizontal_stride = float(horizontal_stride)
        self.vertical_stride = float(vertical_stride)
        self.width_img = float(width_image)
        self.height_img = float(height_image)

        self.move_next_position = True

        self.current_position = [self.left_offset, self.top_offset]

        self.reset_position()

    # ---------------------------------------------------------------------------
    def get_position(self):
        return [int(i) for i in self.current_position]

    # ---------------------------------------------------------------------------
    def get_next_position(self):
        if not self.move_next_position:
            return self.current_position

        if self._get_increase_x() >= (self.width_img - self.right_offset):
            self._reset_x_position()

            if self._get_increase_y() >= (self.height_img - self.bottom_offset):
                self.move_next_position = False
            else:
                self._increase_y()
        else:
            self._increase_x()

        return [int(i) for i in self.current_position]

    # ---------------------------------------------------------------------------
    def has_next_position(self):
        return self.move_next_position

    # ---------------------------------------------------------------------------
    def reset_position(self):
        self._reset_x_position()
        self._reset_y_position()

    # ---------------------------------------------------------------------------
    def _reset_x_position(self):
        self.current_position[0] = self.left_offset

    # ---------------------------------------------------------------------------
    def _reset_y_position(self):
        self.current_position[1] = self.top_offset

    # ---------------------------------------------------------------------------
    def _get_increase_x(self):
        return self.current_position[0] + self.horizontal_stride

    # ---------------------------------------------------------------------------
    def _get_increase_y(self):
        return self.current_position[1] + self.vertical_stride

    # ---------------------------------------------------------------------------
    def _increase_x(self):
        self.current_position[0] = self._get_increase_x()

    # ---------------------------------------------------------------------------
    def _increase_y(self):
        self.current_position[1] = self._get_increase_y()


#######################################################################################################################
from math import sin, cos, pi, acos


class CircularTrajectory(Trajectory):
    def __init__(self, horizontal_stride, vertical_stride, radius_max, radius_min, center_x, center_y, width_image,
                 height_image):

        Trajectory.__init__(self)

        if center_y is None:
            center_y = height_image/2.0

        if center_x is None:
            center_x = width_image/2.0

        if radius_max <= radius_min:
            raise Exception(
                'Error el parametro radiusMax: ' + str(radius_max) + ' debe de ser mayor a radiusMin: ' + str(radius_min))

        if not (0 < center_x < width_image):
            raise Exception(
                'Error centerX: ' + str(center_x) + ' debe de estar entre los valores: (0-' + str(width_image) + ')')

        if not (0 < center_y < height_image):
            raise Exception(
                'Error centerY: ' + str(center_y) + ' debe de estar entre los valores: (0-' + str(height_image) + ')')

        if horizontal_stride >= 2:
            raise Exception('Error horizontalStride debe de ser menor a 2')

        if vertical_stride >= radius_max - radius_min:
            raise Exception('Error verticalStride debe de ser menor a la resta de radiusMax-radiusMin: ' + str(
                radius_max - radius_min))

        self.radius_max = float(radius_max)
        self.radius_min = float(radius_min)
        self.center_x = float(center_x)
        self.center_y = float(center_y)
        self.horizontal_stride = float(horizontal_stride)
        self.vertical_stride = float(vertical_stride)
        self.width_img = float(width_image)
        self.height_img = float(height_image)

        self.move_next_position = True

        self.current_angle = 0.0
        self.current_radius = self.radius_min

        self.current_position = [self.center_x, self.center_y]

    # ---------------------------------------------------------------------------
    def get_position(self):
        return [int(i) for i in self.current_position]

    # ---------------------------------------------------------------------------
    def get_next_position(self):

        if not self.move_next_position:
            return self.current_position

        self._calculate_current_position()

        if self._get_increase_angle() >= 2:
            self._reset_angle()
            if self._get_increase_radius() >= self.radius_max:
                self.move_next_position = False
            else:
                self._increase_radius()
        else:
            self._increase_angle()

        return [int(i) for i in self.current_position]

    # ---------------------------------------------------------------------------
    def has_next_position(self):
        return self.move_next_position

    # ---------------------------------------------------------------------------
    def reset_position(self):
        self.current_position = [self.center_x, self.center_y]
        self._reset_angle()
        self._reset_radius()

    # ---------------------------------------------------------------------------
    def _reset_angle(self):
        self.current_angle = 0

    # ---------------------------------------------------------------------------
    def _reset_radius(self):
        self.current_radius = self.radius_min

    # ---------------------------------------------------------------------------
    def _calculate_current_position(self):
        self._calculate_coordinate_x()
        self._calculate_coordinate_y()

    # ---------------------------------------------------------------------------
    def _calculate_coordinate_y(self):
        self.current_position[1] = sin(self.current_angle * pi) * self.current_radius + self.center_y

    # ---------------------------------------------------------------------------
    def _calculate_coordinate_x(self):
        self.current_position[0] = cos(self.current_angle * pi) * self.current_radius + self.center_x

    # ---------------------------------------------------------------------------
    def _get_increase_angle(self):
        return self.current_angle + self.horizontal_stride

    # ---------------------------------------------------------------------------
    def _get_increase_radius(self):
        return self.current_radius + self.vertical_stride

    # ---------------------------------------------------------------------------
    def _increase_angle(self):
        self.current_angle = self._get_increase_angle()

    # ---------------------------------------------------------------------------
    def _increase_radius(self):
        self.current_radius = self._get_increase_radius()


#######################################################################################################################
if __name__ == '__main__':
    horizontalStride = 0.3
    verticalStride = 70
    radiusMax = 200
    radiusMin = 50
    centerX = 350
    centerY = 300
    widthImage = 703
    heightImage = 627
    trajectory = CircularTrajectory(horizontalStride,
                                    verticalStride,
                                    radiusMax,
                                    radiusMin,
                                    centerX,
                                    centerY,
                                    widthImage,
                                    heightImage)
    print trajectory.get_position()
    while trajectory.has_next_position():
        print trajectory.get_next_position(), 'Angulo: ' + str(trajectory.current_angle), "radio: " + str(
            trajectory.current_radius)

#######################################################################################################################
