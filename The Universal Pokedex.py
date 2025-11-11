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
    def __init__(self, itemGroup, id):
        validGen = False
        self._itemGroup = itemGroup
        self._id = id
        
        if self._itemGroup == 'mon':    #for Mon class
            langDict = {1:1, 2:1, 3:1, 4:1, 5:1, 6:6, 7:7, 8:7, 9:0}   #gen : english index
            self._name = pb.pokemon(id).name
            self._gen = pb.pokemon_species(self._name).generation.id
            self._flavorText = (pb.pokemon_species(id).flavor_text_entries[langDict[self._gen]].flavor_text).replace("\n", " ")

        elif self._itemGroup == 'move': #for Move class
            langDict = {1:6, 2:6, 3:0, 4:0, 5:1, 6:6, 7:7, 8:7, 9:0}   #gen : english index
            self._name = pb.move(id).name
            self._gen = pb.move(self._name).generation.id
            self._flavorText = (pb.move(id).flavor_text_entries[langDict[self._gen]].flavor_text).replace("\n", " ")

        elif self._itemGroup == 'ability':  #for Ability class
            langDict = {3:1, 4:1, 5:1, 6:6, 7:7, 8:7, 9:1}   #gen : english index
            self._name = pb.ability(id).name
            self._gen = pb.ability(self._name).generation.id
            self._flavorText = (pb.ability(id).flavor_text_entries[langDict[self._gen]].flavor_text).replace("\n", " ")
            
    
    def getItemGroup(self):
        return self._itemGroup
    def getItemName(self):
        return self._name
    def getItemID(self):
        return self._id
    def getItemGen(self):
        return self._gen
    def getFlavorText(self):
        return self._flavorText

class Ability(Item):
    def __init__(self, itemGroup, id):
        super().__init__(itemGroup, id)

class Move(Item):
    def __init__(self, itemGroup, id):
        super().__init__(itemGroup, id)
        self._accuracy = pb.move(id).accuracy
        self._effectChance = pb.move(id).accuracy
        self._PP = pb.move(id).pp
        self._priority = pb.move(id).priority
        self._power = pb.move(id).power
        self._dmgClass = pb.move(id).damage_class
        self._target = pb.move(id).target
        self._moveType = pb.move(id).type

        ### sort out statChanges output
        self._statChanges = {'attack':0, 'defense':0, 'special-attack':0, 'special-defense':0, 'speed':0}
        for s in range(len(pb.move(id).stat_changes)):
            self._statChanges[pb.move(id).stat_changes[s].stat] = pb.move(id).stat_changes[s].change

    def getStatChanges(self):
        return self._statChanges

class Mon(Item):
    def __init__(self, itemGroup, id):
        super().__init__(itemGroup, id)
        self._name = pb.pokemon_species(id).name
        self._species = pb.pokemon_species(id).genera[0]
        self._type1 = pb.pokemon(id).types[0].type.name
        try:
            self._type2 = pb.pokemon(id).types[1].type.name
        except IndexError:
            self._type2 = -1
        self._height = pb.pokemon(id).height
        self._weight = (pb.pokemon(id).weight)/10

        self._HP = pb.pokemon(id).stats[0].base_stat
        self._Atk = pb.pokemon(id).stats[1].base_stat
        self._Def = pb.pokemon(id).stats[2].base_stat
        self._SpA = pb.pokemon(id).stats[3].base_stat
        self._SpD = pb.pokemon(id).stats[4].base_stat
        self._Spe = pb.pokemon(id).stats[5].base_stat
        self._BST = self._HP+self._Atk+self._Def+self._SpA+self._SpD+self._Spe

        self._catchRate = pb.pokemon_species(id).capture_rate
        self._eggGroups = []
        for i in pb.pokemon_species(id).egg_groups:
            self._eggGroups.append(i.name)
        self._gender = pb.pokemon_species(id).gender_rate
        self._eggCycle = pb.pokemon_species(id).hatch_counter
        self._evoChainID = pb.pokemon_species(id).evolution_chain.id
        self._evoList = []
        for i in range(len(pb.evolution_chain(self._evoChainID).chain.evolves_to)):
            self._evoList.append(pb.evolution_chain(self._evoChainID).chain.evolves_to[i].species.name)
        try:
            for j in range(len(pb.evolution_chain(self._evoChainID).chain.evolves_to[i].evolves_to)):
                self._evoList.append(pb.evolution_chain(self._evoChainID).chain.evolves_to[i].evolves_to[j].species.name)
        except:
            pass

        try:
            self._preEvo = pb.pokemon_species(id).evolves_from_species.name
        except AttributeError:
            self._preEvo = -1
    
    ##----Methods----##
    def getName(self):
        return self._name
    def getSpecies(self):
        return self._species
    def getType1(self):
        return self._type1
    def getType2(self):
        return self._type2
    def getBST(self):
        return self._BST
    def getHP(self):
        return self._HP
    def getAtk(self):
        return self._Atk
    def getDef(self):
        return self._Def
    def getSpA(self):
        return self._SpA
    def getSpD(self):
        return self._SpD
    def getSpe(self):
        return self._Spe

    def getHeight(self):
        return self._height
    def getWeight(self):
        return self._weight
    def getCatchRate(self):
        return self._catchRate
    def getEggGroups(self):
        return self._eggGroups
    def getEvoList(self):
        return self._evoList
    def getPreEvo(self):
        return self._preEvo

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

# myItem = Move('move', 370)
# name = myItem.getItemName()
# flavorText = myItem.getFlavorText()
# generation = myItem.getItemGen()
# statChanges = myItem.getStatChanges()
# print(name)
# print(flavorText)
# print(generation)
# for i in statChanges:
#     print(i)

myMon = Mon('mon', 840)
# type1 = myMon.getType1()
# type2 = myMon.getType2()
# HP = myMon.getHP()
# Atk = myMon.getAtk()
# Def = myMon.getDef()
# SpA = myMon.getSpA()
# SpD = myMon.getSpD()
# Spe = myMon.getSpe()
# BST = myMon.getBST()
# stats = [BST, HP, Atk, Def, SpA, SpD, Spe]
evoList = myMon.getEvoList()
preEvo = myMon.getPreEvo()
name = myMon.getName()
# print(type1)
# print(type2)
# print(stats)
print(name)
print(evoList)
print(preEvo)