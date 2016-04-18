# -*- coding: utf-8 -*-

__author__ = 'isaac'

import pygame
from pygame import mixer

class AudioPlayer:

    def __init__(self):
        self.alias = "[AP]>> "
        self.audioPath = "audio/"
        self.audioFormat = ".wav"
        print self.alias , "Audio Player Initialized"


    def play(self, audio):
        #pygame.init()
        print self.alias, "Reproduciendo sonido para clase ", audio
        mixer.music.load(self.audioPath + audio + self.audioFormat)
        mixer.music.play(0)
        clock = pygame.time.Clock()
        clock.tick(10)
        while mixer.music.get_busy():
            pygame.event.poll()
            clock.tick(10)



# Si se ejecuta desde aquí funciona bien y reproduce el audio, pero da problemas al hacer llamadas desde otros módulos

#reproductor = AudioPlayer()
#reproductor.play("perro")
#reproductor.play("gato")
#reproductor.play("desconocido")
