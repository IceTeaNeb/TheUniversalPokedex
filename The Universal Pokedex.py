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
    print(pb.pokemon(pNameID).weight)
    print(pb.pokemon(pNameID).height)
        

nameOrID = int(input("Enter name (0) or ID (1)? "))
if nameOrID == 0:
    monName = int(input("Enter name of Pokémon: "))
elif nameOrID == 1:
    monID = int(input("Enter ID of Pokémon: "))

showInfo(pNameID)
