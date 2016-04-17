from ParserHandler import get_environment_cfg

resource_handler = get_environment_cfg()


def getNeuralNetworks(environment):
    resource_handler.get(environment, 'redes_neuronales_ids')
    pass