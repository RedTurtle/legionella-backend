# -*- coding: utf-8 -*-
from .models import Floor


class FloorMutationService(object):
    def createFloor(self, input):
        """
        creazione di un nuovo floor
        input:
            input: dict coni parametri per la creazione
        output:
            istanza del modello di Floor
        """
        floorlabel = input.get('label')

        piano = Floor(label=floorlabel)
        piano.save()

        return piano
