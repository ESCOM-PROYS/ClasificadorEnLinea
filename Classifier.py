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
from Trajectories import SimpleTrajectory, CircularTrajectory
from Segmenters import RectangularSegmenter
import PIL
from PIL.Image import open
from ParserHandler import get_circular_trajectory, get_rectangular_segmenter



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
                        pygame.mixer.music.load("perro.wav")
                        self.takePicture()
                        #Para pruebas de reproducción --- (En mi compu no furula)
                        self.play("perro")
                        self.play("gato")
                        self.play("desconocido")
                        # -------------------------------
                        self.startClasification()
                        print self.alias, "UP: ", holdTime
                        holdTime = 0
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
        #numImages = self.imageProcesor.runSegmentation("img/photo.jpg")
        numImages = self.segment_entry_image("img/photo.jpg", 'img/segments/')
        for imageIndex in range(numImages):
            self.neuralNetwork.classifyImage('img/segments/cutout'+str(imageIndex)+'.jpg' , imageIndex)


    def segment_entry_image(self, url_image, url_output):
        img = open(url_image)

        width_image, height_image = img.size
        trajectory = get_circular_trajectory(width_image, height_image)
        segmenter = get_rectangular_segmenter(img, trajectory)

        i = 0
        image = segmenter.get_current_segment()
        image.pil_image.save(url_output+'cutout' + str(i) + '.jpg')

        i += 1
        while (segmenter.has_next_segment()):
            image = segmenter.get_next_segment()
            image.pil_image.save(url_output+'cutout' + str(i) + '.jpg')
            i += 1
        return i


    def play(self, audio):
        #pygame.init()
        print self.alias, "Reproduciendo sonido para clase ", audio
        pygame.mixer.music.load(self.audioPath + audio + self.audioFormat)
        pygame.mixer.music.play(0)
        clock = pygame.time.Clock()
        clock.tick(10)
        while pygame.mixer.music.get_busy():
            pygame.event.poll()
            clock.tick(10)
