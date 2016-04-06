__author__ = 'isaac'
import numpy as np
import pygame
import os
import matplotlib.pyplot as plt
from random import shuffle
import caffe
import os
import sys


class NeuralNetwork:

    def __init__(self, netModel, netPrototype, netMean , classesList, environmentsList):
        self.netClasses = classesList
        self.environments = environmentsList
        self.home = os.getenv("HOME")
        self.caffe_root = self.home + '/caffe/'
        sys.path.insert(0, self.caffe_root + 'python')
        errorFlag = False
        print("Buscando un modelo pre entrenado CaffeNet-model...")
        if not os.path.isfile(netModel) or not os.path.isfile(netPrototype):
            print "No es posible cargar la red neuronal. No se encuentra el modelo de la red"
            errorFlag = True
        else:
            self.netModel = netModel
            print 'Modelo de la red neuronal cargado'
        if not os.path.isfile(netPrototype):
            print "No es posible cargar la red neuronal. No se encuentra el prototipo de la red"
            errorFlag = True
        else:
            self.netPrototype = netPrototype
            print 'Prototipo de la red neuronal cargado'
        if not os.path.isfile(netMean):
            print "No es posible cargar el archivo que contiene la media de las imagenes"
            errorFlag = True
        else:
            print "Media cargada."
        if not errorFlag:
            self.configureNetwork()

    def configureNetwork(self):
        caffe.set_mode_cpu()
        self.neuralNetwork = caffe.Net(self.netPrototype, self.netModel, caffe.TEST)
        print 'Red cargada exitosamente.'
        blobm = caffe.proto.caffe_pb2.BlobProto()
        datam = open( self.netMean, 'rb' ).read()
        blobm.ParseFromString(datam)
        mx = np.array(blobm.data)
        print mx.shape
        my = np.reshape(mx,(3,256,256))
        print 'shape mean',my.shape
        mean = my.mean(1).mean(1)
        print "Media: ", mean
        self.transformer = caffe.io.Transformer({'data': self.neuralNetwork.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2,0,1))
        self.transformer.set_raw_scale('data', 255)         # El modelo de referencia opera en imagenes en rango [0,255] en lugar de [0,1]
        self.transformer.set_channel_swap('data', (2,1,0))  # El modelo de referencia tiene canales BGR en lugar de RGB
        # set net to batch size of 50
        self.neuralNetwork.blobs['data'].reshape(1,3,256,256)

    def getNet(self):
        return self

    def getNetClasses(self):
        return self.netClasses

    def getNetEnvironments(self):
        return self.environments


    def classifyImage(self, rutaImagen):
        self.neuralNetwork.blobs['data'].data[...] = self.transformer.preprocess('data', caffe.io.load_image(rutaImagen))
        out = self.neuralNetwork.forward()
        #plt.imshow(transformer.deprocess('data', net.blobs['data'].data[0]))
        # #plt.show()
        print("Clase detectada: " , self.netClasses[out['prob'].argmax()])

