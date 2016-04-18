from ParserHandler import *

resource_handler_environment = get_environment_cfg()
resource_handler_NN = get_neural_network_cfg()


def get_all_neural_networks(environment_id):
    """
    Return all the neural networks than belonging to the given environment
    :param environment_id:environment's id where neural networks will be obtained, must be a string
    :return: a list of neural network
    """
    ids = resource_handler_environment.get(str(environment_id),
                                           property_name_environment_cfg_neural_network_ids).split(default_separator)

    neural_networks = (_build_neural_network(str(neural_network_id)) for neural_network_id in ids)

    return neural_networks


def get_neural_network_by_priority(environment_id, priority):
    """
    Return a neural network according to the priority given
    :param environment_id: environment's name where neural network will be obtained, must be a string
    :param priority: value between 0 to 100, where 0 is the last neural network, and 100 are the first neural network
    :return: a neural network
    """
    ids = resource_handler_environment.get(str(environment_id),
                                           property_name_environment_cfg_neural_network_ids).split(default_separator)
    if priority == 100:
        return _build_neural_network(str(ids[0]))
    if priority == 0:
        return _build_neural_network(str(ids[len(ids) - 1]))

    target_id = str((len(ids) - 1) - (int((priority*len(ids))/100) - 1))

    return _build_neural_network(target_id)


def _build_neural_network(neural_network_id):
    network_model = resource_handler_NN.get(neural_network_id, property_name_net_descriptor_model)
    network_mean = resource_handler_NN.get(neural_network_id, property_name_net_descriptor_mean)
    network_prototype = resource_handler_NN.get(neural_network_id, property_name_net_descriptor_prototype)
    network_classes = resource_handler_NN.get(neural_network_id,
                                              property_name_net_descriptor_classes).split(default_separator)

    return network_model, network_mean, network_prototype, network_classes


if __name__ == '__main__':
    for a in get_all_neural_networks('1'):
        print a