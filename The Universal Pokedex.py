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

#def Main():




class Item:
    def __init__(self, itemGroup, id, gen):
        self._itemGroup = itemGroup
        self._id = id
        
        while validIn == True:
            if self._itemGroup == 'mon':
                langDict = {1:1, 2:1, 3:1, 4:1, 5:1, 6:6, 7:7, 8:7, 9:0}   #gen : english index
                self._gen = pb.pokemon(id).
                self._name = pb.pokemon(id).name
                self._flavorText = (pb.pokemon_species.flavor_text_entries[langDict[gen]].flavor_text).replace("\n", " ")

            elif self._itemGroup == 'move':
                langDict = {1:6, 2:6, 3:0, 4:0, 5:1, 6:6, 7:7, 8:7, 9:0}   #gen : english index
                self._name = pb.move(id).name
                self._flavorText = (pb.move(id).flavor_text_entries[langDict[gen]].flavor_text).replace("\n", " ")

            elif self._itemGroup == 'ability':
                langDict = {3:1, 4:1, 5:1, 6:6, 7:7, 8:7, 9:1}   #gen : english index
                self._name = pb.ability(id).name
                self._flavorText = (pb.ability(id).flavor_text_entries[langDict[gen]].flavor_text).replace("\n", " ")
    
    def getItemGroup(self):
        return self._itemGroup
    def getItemName(self):
        return self._name
    def getItemID(self):
        return self._ID
    def getItemGen(self):
        return self._gen
    def getFlavorText(self):
        return self._flavorText

class Ability(Item):
    def __init__(self, itemGroup, id, gen):
        super().__init__(itemGroup, id, gen)

class Move(Item):
    def __init__(self, itemGroup, id, gen):
        super().__init__(itemGroup, id, gen)
        self._accuracy = pb.move(id).accuracy
        self._effectChance = pb.move(id).accuracy
        self._PP = pb.move(id).pp
        self._priority = pb.move(id).priority
        self._power = pb.move(id).power
        self._dmgClass = pb.move(id).damage_class
        self._target = pb.move(id).target
        self._moveType = pb.move(id).type
        self._statChanges = {'attack':0, 'defense':0, 'special-attack':0, 'special-defense':0, 'speed':0}
        for s in range(len(pb.move(id).stat_changes)):
            self._statChanges[pb.move(id).stat_changes[s].stat] = pb.move(id).stat_changes[s].change

# class Mon(Item):
#     def __init__(self, itemGroup, id, gen):
#         super().__init__(itemGroup, id, gen)
#         self._species = pb.genera(id).genus

# inID = int(input("enter id: "))
# #print(pb.pokemon(inID).name)
# #print((pb.pokemon_species(inID).flavor_text_entries[0].flavor_text).replace("\n", " "))

# print(pb.move(inID).name)
# print((pb.move(inID).flavor_text_entries[0].flavor_text).replace("\n", " "))
# for i in range(len(pb.move(inID).stat_changes)):
#     print(pb.move(inID).stat_changes[i].stat)
#     print(pb.move(inID).stat_changes[i].change)

#print(pb.ability(inID).name)
#print((pb.ability(inID).flavor_text_entries[1].flavor_text).replace("\n", " "))


# def itemInfo():
#     itemType = input("Enter Item Type: ")
#     if itemType == 'mon':
#         myMon = Mon

myMove = Move('move', 370, 4)
flavorText = myMove.getFlavorText()
print(flavorText)