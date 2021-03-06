# -*- coding: utf-8 -*-
__author__ = 'isaac'
import numpy as np
import os
import sys
from pygame import mixer
from AudioPlayer import *

home = os.getenv("HOME")
caffe_root = home + '/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe

class NeuralNetwork:

    def __init__(self, netModel, netPrototype, netMean , classesList):
        self.alias = "[NNET]>> "
        self.netClasses = classesList
        self.defaultClass = "desconocido"
        self.speaker = AudioPlayer()
        #self.environments = environmentsList
        #self.home = os.getenv("HOME")
        #self.caffe_root = self.home + '/caffe/'
        #sys.path.insert(0, self.caffe_root + 'python')

        errorFlag = False
        print self.alias , "Buscando un modelo pre entrenado CaffeNet-model..."
        if not os.path.isfile(netModel) or not os.path.isfile(netPrototype):
            print self.alias , "No es posible cargar la red neuronal. No se encuentra el modelo de la red"
            errorFlag = True
        else:
            self.netModel = netModel
            print self.alias , 'Modelo de la red neuronal cargado'
        if not os.path.isfile(netPrototype):
            print self.alias , "No es posible cargar la red neuronal. No se encuentra el prototipo de la red"
            errorFlag = True
        else:
            self.netPrototype = netPrototype
            print self.alias , 'Prototipo de la red neuronal cargado'
        if not os.path.isfile(netMean):
            print self.alias , "No es posible cargar el archivo que contiene la media de las imagenes"
            errorFlag = True
        else:
            self.netMean = netMean
            print self.alias , "Media cargada."
        if not errorFlag:
            self.configureNetwork()
        else:
            print self.alias,  "Ocurrió un error al intentar cargar la red neuronal."
        print self.alias, netModel
        print self.alias, netPrototype
        print self.alias, netMean
        print self.alias, classesList


    def configureNetwork(self):
        caffe.set_mode_cpu()
        self.neuralNetwork = caffe.Net(self.netPrototype, self.netModel, caffe.TEST)
        print self.alias , 'Red cargada exitosamente.'
        blobm = caffe.proto.caffe_pb2.BlobProto()
        datam = open(self.netMean, 'rb' ).read()
        blobm.ParseFromString(datam)
        mx = np.array(blobm.data)
        print self.alias ,  mx.shape
        my = np.reshape(mx, (3, 256, 256))
        print self.alias, 'shape mean', my.shape
        mean = my.mean(1).mean(1)
        print self.alias , "Media: ", mean
        self.transformer = caffe.io.Transformer({'data': self.neuralNetwork.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2, 0, 1))
        self.transformer.set_raw_scale('data', 255)         # El modelo de referencia opera en imagenes en rango [0,255] en lugar de [0,1]
        self.transformer.set_channel_swap('data', (2, 1, 0))  # El modelo de referencia tiene canales BGR en lugar de RGB
        self.neuralNetwork.blobs['data'].reshape(1, 3, 256, 256)


    def getNet(self):
        return self

    def getNetClasses(self):
        return self.netClasses

    def getNetEnvironments(self):
        return self.environments

    def classifyImage(self, imagePath, imageIndex):
        self.neuralNetwork.blobs['data'].data[...] = self.transformer.preprocess('data', caffe.io.load_image(imagePath))
        out = self.neuralNetwork.forward()
        #plt.imshow(transformer.deprocess('data', net.blobs['data'].data[0]))
        #plt.show()
        argmaxArray = out['prob'][out['prob'].argmax()]
        maxProbabilityIndex = out['prob'][out['prob'].argmax()].argmax()
        detectedClass = ""
        #print self.alias, "Clase detectada: ", str(imageIndex), self.netClasses[out['prob'].argmax()], " - ", self.neuralNetwork.blobs['prob'].data , "  >> " , argmaxArray[maxProbabilityIndex]
        if argmaxArray[maxProbabilityIndex] > 0.65:
            detectedClass = self.netClasses[out['prob'].argmax()]
            print self.alias, "Clase detectada: ", str(imageIndex), detectedClass,  " Probabilidad >> ", argmaxArray[maxProbabilityIndex]
        else:
            detectedClass = self.defaultClass
            print self.alias, "Clase ", detectedClass
        #self.speaker.play(detectedClass)

