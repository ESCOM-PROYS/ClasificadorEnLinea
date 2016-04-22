import ConfigParser
from Trajectories import CircularTrajectory, SimpleTrajectory
from Segmenters import RectangularSegmenter

object_parser = None
environment_parser = None
neural_network_parser = None
segmenter_parser = None


def get_environment_cfg():
    global environment_parser
    if environment_parser is None:
        environment_parser = _build_config_parser(url_file_cfg_environment)
    return environment_parser


def get_object_cfg():
    global object_parser
    if object_parser is None:
        object_parser = _build_config_parser(url_file_cfg_object)
    return object_parser


def get_segmenter_cfg():
    global segmenter_parser
    if segmenter_parser is None:
        segmenter_parser = _build_config_parser(url_file_cfg_segmenter)
    return segmenter_parser


def get_circular_trajectory(width_image, height_image):
    parser = get_segmenter_cfg()
    horizontal_stride = parser.getfloat(section_name_circular_trajectory, prop_name_cir_tra_horizontal_stride)
    vertical_stride = parser.getfloat(section_name_circular_trajectory, prop_name_cir_tra_vertical_stride)
    radius_max = parser.getfloat(section_name_circular_trajectory, prop_name_cir_tra_radius_max)
    radius_min = parser.getfloat(section_name_circular_trajectory, prop_name_cir_tra_radius_min)
    center_x = parser.getfloat(section_name_circular_trajectory, prop_name_cir_tra_center_x)
    center_y = parser.getfloat(section_name_circular_trajectory, prop_name_cir_tra_center_y)

    circular_trajectory = CircularTrajectory(horizontal_stride,
                                             vertical_stride,
                                             radius_max,
                                             radius_min,
                                             center_x,
                                             center_y,
                                             width_image,
                                             height_image)

    return circular_trajectory


def get_simple_trajectory(width_image, height_image):
    parser = get_segmenter_cfg()
    horizontal_stride = parser.getfloat(section_name_simple_trajectory, prop_name_sim_tra_horizontal_stride)
    vertical_stride = parser.getfloat(section_name_simple_trajectory, prop_name_sim_tra_vertical_stride)
    top_offset = parser.getfloat(section_name_simple_trajectory, prop_name_sim_tra_top_offset)
    bottom_offset = parser.getfloat(section_name_simple_trajectory, prop_name_sim_tra_bottom_offset)
    right_offset = parser.getfloat(section_name_simple_trajectory, prop_name_sim_tra_right_offset)
    left_offset = parser.getfloat(section_name_simple_trajectory, prop_name_sim_tra_left_offset)

    simple_trajectory = SimpleTrajectory(horizontal_stride,
                                         vertical_stride,
                                         top_offset,
                                         left_offset,
                                         right_offset,
                                         bottom_offset,
                                         width_image,
                                         height_image)

    return simple_trajectory


def get_rectangular_segmenter(img, trajectory):
    parser = get_segmenter_cfg()
    segmenter = RectangularSegmenter(img,
                                     parser.getint(section_name_rectangular_segmenter, prop_name_rec_seg_height_cut),
                                     parser.getint(section_name_rectangular_segmenter, prop_name_rec_seg_width_cut),
                                     trajectory)
    return segmenter


def get_neural_network_cfg():
    global neural_network_parser
    if neural_network_parser is None:
        neural_network_parser = _build_config_parser(url_file_cfg_net_descriptor)
    return neural_network_parser


def _build_config_parser(url_file_cfg):
    config = ConfigParser.RawConfigParser()
    config.read(url_file_cfg)
    return config


default_separator = ','

url_file_cfg_environment = 'config/Environment.properties'
url_file_cfg_object = 'config/Object.properties'
url_file_cfg_net_descriptor = 'config/NetDescriptor2.properties'
url_file_cfg_segmenter = 'config/Segmenter.cfg'

property_name_environment_cfg_neural_network_ids = 'neural_networks_ids'
property_name_environment_cfg_name = 'name'
property_name_environment_cfg_frequently_objects = 'frequently_objects'

property_name_object_cfg_name = 'name'

property_name_net_descriptor_environment = 'net.environment'
property_name_net_descriptor_model = 'net.model'
property_name_net_descriptor_mean = 'net.mean'
property_name_net_descriptor_prototype = 'net.prototype'
property_name_net_descriptor_classes = 'net.classes'
property_name_net_descriptor_name = 'net.name'

section_name_circular_trajectory = 'CIRCULAR_TRAJECTORY'
prop_name_cir_tra_horizontal_stride = 'circular_trajectory_horizontal_stride'
prop_name_cir_tra_vertical_stride = 'circular_trajectory_vertical_stride'
prop_name_cir_tra_radius_max = 'circular_trajectory_radius_max'
prop_name_cir_tra_radius_min = 'circular_trajectory_radius_min'
prop_name_cir_tra_center_x = 'circular_trajectory_center_x'
prop_name_cir_tra_center_y = 'circular_trajectory_center_y'

section_name_simple_trajectory = 'SIMPLE_TRAJECTORY'
prop_name_sim_tra_horizontal_stride = 'simple_trajectory_horizontal_stride'
prop_name_sim_tra_vertical_stride = 'simple_trajectory_vertical_stride'
prop_name_sim_tra_top_offset = 'simple_trajectory_top_offset'
prop_name_sim_tra_bottom_offset = 'simple_trajectory_bottom_offset'
prop_name_sim_tra_right_offset = 'simple_trajectory_right_offset'
prop_name_sim_tra_left_offset = 'simple_trajectory_left_offset'

section_name_rectangular_segmenter = 'RECTANGULAR_SEGMENTER'
prop_name_rec_seg_width_cut = 'rectangular_segmenter_width_cut'
prop_name_rec_seg_height_cut = 'rectangular_segmenter_height_cut'

if __name__ == '__main__':
    a = get_environment_cfg()
    print a.get('1', property_name_environment_cfg_name)
