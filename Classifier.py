# -*- coding: utf-8 -*-
__author__ = 'isaac'

import pygame
import numpy as np
import os
import sys
from NeuralNetworksHandler import NeuralNetworksHandler
from NeuralNetwork import  NeuralNetwork
from ImagePreprocesor import ImagePreprocesor
from AudioPlayer import AudioPlayer
import matplotlib.pyplot as plt
from random import shuffle


class Classifier:

    def __init__(self):
        self.alias = "[CLASSIFIER]>> "
        print self.alias , "Iniciando Clasificador..."
        self.netHandler = NeuralNetworksHandler()
        self.imageProcesor = ImagePreprocesor(wideSegment=150, highSegment=150, horizontalStride=50, verticalStride=50, withResizeImgOut=250, highResizeImgOut=250)
        networkModel, netMean, prototype, classes = self.netHandler.getNetworkByIndex(0)
        self.neuralNetwork = NeuralNetwork(networkModel,  prototype, netMean, classes)
        self.speaker = AudioPlayer()
        self.eventListener()


    def eventListener(self):
        tickTime = pygame.time.Clock()
        holdTime = 0
        pygame.init()
        DISPLAYSURF = pygame.display.set_mode((900, 900))
        DISPLAYSURF.fill((255, 255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    holdTime = tickTime.tick(60)
                    print self.alias, "DOWN: ", holdTime
                if event.type == pygame.MOUSEBUTTONUP:
                    if holdTime < 3000:
                        print "----------------------------"
                        print self.alias, "CLASSIFYING... "
                        print "----------------------------"
                        self.takePicture()
                        self.startClasification()
                        print self.alias, "UP: ", holdTime
                        holdTime = 0
                        #Para pruebas de reproducción --- (En mi compu no furula)
                        self.speaker.play("perro")
                        self.speaker.play("gato")
                        self.speaker.play("desconocido")
                        # -------------------------------
                    else:
                        print self.alias, ": ", holdTime, " miliSegundos"
                        networkModel, netMean, prototype, classes = self.netHandler.getNextNet()
                        self.neuralNetwork = NeuralNetwork(networkModel, netMean, prototype, classes)
                        holdTime = 0
                if event.type == pygame.QUIT:
                    sys.exit(0)

    def takePicture(self):
        print self.alias , "Adquiriendo imagen"
        os.system("bash AdquisidorImagenes.sh")

    def startClasification(self):
        print self.alias, "Clasificando objetos en imágen"
        numImages = self.imageProcesor.runSegmentation("img/photo.jpg")
        for imageIndex in range(numImages-1):
            self.neuralNetwork.classifyImage('img/segments/cutout'+str(imageIndex)+'.jpg', imageIndex)

