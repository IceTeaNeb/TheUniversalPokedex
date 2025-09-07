#The Universal Pokedex

#----------------------LIBRARIES----------------------#
import pokebase as pb
import tkinter as tk
import PIL
from tkinter import PhotoImage, ttk
from PIL import Image, ImageTk
from ctypes import windll
#-----------------------------------------------------#

def showInfo(pNameID):
    print('Name: ' + pb.pokemon(pNameID).name)
    print('ID: ' + str(pb.pokemon(pNameID).id))
    print('Weight: ' + str(pb.pokemon(pNameID).weight))
    print('Height: ' + str(pb.pokemon(pNameID).height))
    print('Order: ', str(pb.pokemon(pNameID).order))
        

nameOrID = int(input("Enter name (0) or ID (1)? "))
if nameOrID == 0:
    monName = input("Enter name of Pokémon: ")
    showInfo(monName.lower())
elif nameOrID == 1:
    monID = int(input("Enter ID of Pokémon: "))
    showInfo(monID)
