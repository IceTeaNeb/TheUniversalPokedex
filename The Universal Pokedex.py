#The Universal Pokedex

#----------------------LIBRARIES----------------------#
import pokebase as pb
import tkinter as tk
import PIL
import requests
from tkinter import PhotoImage, ttk
from PIL import Image, ImageTk
from ctypes import windll
#-----------------------------------------------------#


class Pokemon():
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.weight = pb.pokemon(id).weight
        self.height = pb.pokemon(id).height
        self.moves = pb.pokemon(id).moves

    def showInfo(self):
        print('Name: ' + self.name)
        print('ID: ' + str(self.id))
        print('Height: ' + str(self.weight))
        print('Weight: ' + str(self.height))
        print('Moves: ' + ', '.join([move.move.name for move in self.moves]))

class SubMon(Pokemon):      #subclass of Pokemon
    def __init__(self, id, name):
        super().__init__(id, name)
        self.type = pb.pokemon(id).types

    def showType(self):
        print(self.type)

def showInfo(pID):
    print('Name: ' + pb.pokemon(pID).name)
    print('ID: ' + str(pb.pokemon(pID).id))
    print('Weight: ' + str(pb.pokemon(pID).weight))
    print('Height: ' + str(pb.pokemon(pID).height))
    print('Order: ', str(pb.pokemon(pID).order))
        
monName = input("Enter name of Pokémon: ").lower()
monID = pb.pokemon(monName).id
#showInfo(monID)

pokemon = SubMon(monID, monName.lower())
pokemon.showInfo()
pokemon.showType()
#print(pb.pokemon(monID).types)

