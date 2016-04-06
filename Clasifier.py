__author__ = 'isaac'
import pygame
import numpy as np
import os
import matplotlib.pyplot as plt
from random import shuffle



class Classifier:

    def __init__(self):
        print " "

    def eventListener(self):
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((900, 900))
        DISPLAYSURF.fill((255, 255, 255,255))
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONUP ):
                    print "Clasificando..."
                    self.takePicture()


                    #os.system("date")
                    #clasificar("img/dog.jpg")
                    #clasificar("img/cat.jpg")
                #if (event.type == pygame.MOUSEBUTTONDOWN ):
                    # contar segundos transcurridos
                    # cambiar red neruonal si 3 segundos


    def takePicture(self):
        print "Adquiriendo imagen"
        os.system("date")
