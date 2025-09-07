#The Universal Pokedex

#----------------------LIBRARIES----------------------#
import pokebase as pb
import tkinter as tk
import PIL
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

    def showInfo(self):
        print('Name: ' + self.name)
        print('ID: ' + str(self.id))
        print('Height: ' + str(self.weight))
        print('Weight: ' + str(self.height))

class SubMon(Pokemon):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.type = pb.pokemon(id).

#def showInfo(pID):
    #print('Name: ' + pb.pokemon(pID).name)
    #print('ID: ' + str(pb.pokemon(pID).id))
    #print('Weight: ' + str(pb.pokemon(pID).weight))
    #print('Height: ' + str(pb.pokemon(pID).height))
    #print('Order: ', str(pb.pokemon(pID).order))
        
monName = input("Enter name of Pokémon: ").lower()
monID = pb.pokemon(monName).id
#showInfo(monID)

pokemon = Pokemon(monID, monName.lower())
pokemon.showInfo()

