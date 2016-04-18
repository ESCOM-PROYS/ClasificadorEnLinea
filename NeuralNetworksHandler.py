__author__ = 'isaac'

import ConfigParser
from EnvironmentHandler import get_all_neural_networks, get_neural_network_by_priority

class NeuralNetworksHandler:

    def __init__(self):
        self.alias = "[NNH]>> "
        print self.alias, "Neural Network Hadler Initialized"
        self.currentNet = 0
        self.availableNets = 0
        self.configFile = ""
        self.netDescriptorSections = []
        self.loadNetworksCatalog()

    def loadNetworksCatalog(self):
        print self.alias , "Reading available networks description..."
        self.configFile = ConfigParser.RawConfigParser()
        self.configFile.read("config/NetDescriptor.properties")
        self.netDescriptorSections = self.configFile.sections()
        self.availableNets = len(self.netDescriptorSections)
        print self.alias , " Available networks: \n", self.netDescriptorSections

    def getAvailableNets(self):
        return self.availableNets
        
    def getSectionOption(self , sectionName , option):
        return self.configFile.get(sectionName, option)

    def getNetworkByEnvironmet(self, environment):
        """
        :param environment:this parameter must be a integer, which represents environment's identifier
        :return: a neural network
        """
        print self.alias , "Searching for Environment : " , environment
        return get_neural_network_by_priority(str(environment), 100)
        #search for environments through options
        #return networkModel, netMean, prototype , classes

    def getNetworkByIndex(self, index):
        if self.currentNet < self.availableNets:
            print self.alias , "Searching for network " , index
            networkModel = self.getSectionOption(self.netDescriptorSections[self.currentNet] , 'net.model')
            netMean = self.getSectionOption(self.netDescriptorSections[self.currentNet], 'net.mean')
            prototype = self.getSectionOption(self.netDescriptorSections[self.currentNet], 'net.prototype')
            classes = (self.getSectionOption(self.netDescriptorSections[self.currentNet], 'net.classes')).split(',')
            return networkModel, netMean, prototype , classes
        else:
            return None

    def getNextNet(self):
        if self.currentNet < self.availableNets:
            self.currentNet += 1
        else:
            self.currentNet = 0
        return self.getNetworkByIndex(self.currentNet)

