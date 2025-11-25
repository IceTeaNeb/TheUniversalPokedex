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

#---------Item Class---------#
class Item:
    def __init__(self, itemGroup, id):

        ##---------Attributes---------##
        validGen = False
        self._itemGroup = itemGroup
        self._id = id
        
        if self._itemGroup == 'mon':    #for Mon class
            langDict = {1:1, 2:1, 3:1, 4:1, 5:1, 6:6, 7:7, 8:7, 9:0}   #gen : english index
            self._name = pb.pokemon(id).name    ##name of pokemon
            self._gen = pb.pokemon_species(id).generation.id    ##generation introduced
            self._flavorText = (pb.pokemon_species(id).flavor_text_entries[langDict[self._gen]].flavor_text).replace("\n", " ") ##pokemon flavor text

        elif self._itemGroup == 'move': #for Move class
            langDict = {1:6, 2:6, 3:0, 4:0, 5:1, 6:6, 7:7, 8:7, 9:0}   #gen : english index
            self._name = pb.move(id).name   ##name of move
            self._gen = pb.move(self._name).generation.id   ##generation introduced
            self._flavorText = (pb.move(id).flavor_text_entries[langDict[self._gen]].flavor_text).replace("\n", " ")    ##move flavor text

        elif self._itemGroup == 'ability':  #for Ability class
            langDict = {3:1, 4:1, 5:1, 6:6, 7:7, 8:7, 9:1}   #gen : english index
            self._name = pb.ability(id).name    ##name of ability
            self._gen = pb.ability(self._name).generation.id    ##generation introduced
            self._flavorText = (pb.ability(id).flavor_text_entries[langDict[self._gen]].flavor_text).replace("\n", " ") ##ability flavor text
            
    ##---------Methods---------#
    ##getter methods
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

#---------Ability Class---------#
class Ability(Item):
    def __init__(self, itemGroup, id):
        super().__init__(itemGroup, id)

#---------Move Class---------#
class Move(Item):
    def __init__(self, itemGroup, id):

        ##---------Attributes---------##
        super().__init__(itemGroup, id)
        self._accuracy = pb.move(id).accuracy   ##percentage of success
        self._effectChance = pb.move(id).effect_chance  ##percentage of effect success
        self._PP = pb.move(id).pp   ##power points, number of times move can be used
        self._priority = pb.move(id).priority   ##value between -8 and 8 determining the order of move execution
        self._power = pb.move(id).power ##base power of move
        self._dmgClass = pb.move(id).damage_class   ##type of damage the move inflicts
        self._target = pb.move(id).target   ##type of target that will receive the effect of the move
        self._moveType = pb.move(id).type   ##elemental type of the move
        self._statChanges = {}   ##stats the moves affects and how much it affects them
        for s in range(len(pb.move(id).stat_changes)):
            self._statChanges[pb.move(id).stat_changes[s].stat.name] = pb.move(id).stat_changes[s].change

    ##---------Methods---------##
    ##getter methods
    def getAccuracy(self):
        return self._accuracy
    def getEffectChance(self):
        return self._effectChance
    def getPP(self):
        return self._PP
    def getPriority(self):
        return self._priority
    def getPower(self):
        return self._power
    def getDmgClass(self):
        return self._dmgClass
    def getTarget(self):
        return self._target
    def getType(self):
        return self._moveType
    def getStatChanges(self):
        return self._statChanges

#---------Pokémon Class---------#
class Mon(Item):
    def __init__(self, itemGroup, id):

        ##---------Attributes---------##
        super().__init__(itemGroup, id)
        self._species = pb.pokemon_species(id).genera[0]
        self._type1 = pb.pokemon(id).types[0].type.name
        try:
            self._type2 = pb.pokemon(id).types[1].type.name
        except IndexError:  ###if pokemon has only one type
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

        self._evoList = []  ###first sublist is base of evolution chain, all subsequent sublists represent a branch of the evolution chain
        self._evoList.append([pb.evolution_chain(self._evoChainID).chain.species.name])
        for i in range(len(pb.evolution_chain(self._evoChainID).chain.evolves_to)):
            evoBranchList = []
            evoBranchList.append(pb.evolution_chain(self._evoChainID).chain.evolves_to[i].species.name)
            try:
                for j in range(len(pb.evolution_chain(self._evoChainID).chain.evolves_to[i].evolves_to)):
                    evoBranchList.append(pb.evolution_chain(self._evoChainID).chain.evolves_to[i].evolves_to[j].species.name)
            except: ###to prevent program crashing
                pass
            self._evoList.append(evoBranchList)
        try:
            self._preEvo = pb.pokemon_species(id).evolves_from_species.name
        except AttributeError:  ###to show pokemon has no pre-evolution
            self._preEvo = -1

        self._locations = []
        for j in range(len(pb.pokemon(id).location_area_encounters)):
            self._locations.append(pb.pokemon(id).location_area_encounters[j].location_area.name)

    ##---------Methods---------##
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
    def getLocations(self):
        return self._locations

def menu():
    userIn = int(input("[0]: Pokémon Details\n[1]: Move Details\n[2]: Ability Details\nEnter Option:"))
    if userIn == 0:
        outMon()
    elif userIn == 1:
        outMove()
    elif userIn == 2:
        outAbility()

def outMon():
    monID = int(input("Enter Pokémon ID: "))
    myMon = Mon('mon', monID)
    type1 = myMon.getType1()
    type2 = myMon.getType2()
    HP = myMon.getHP()
    Atk = myMon.getAtk()
    Def = myMon.getDef()
    SpA = myMon.getSpA()
    SpD = myMon.getSpD()
    Spe = myMon.getSpe()
    BST = myMon.getBST()
    stats = [BST, HP, Atk, Def, SpA, SpD, Spe]
    evoList = myMon.getEvoList()
    preEvo = myMon.getPreEvo()
    name = myMon.getItemName()
    locations = myMon.getLocations()

    print('Name: ' + name)
    print('Type 1: ', type1)
    print('Type 2: ', type2)
    print('Stats [BST, HP, Atk, Def, SpA, SpD, Spe]: ', stats)
    print('Evolution Chain: ', evoList)
    print('Pre-Evolution: ', preEvo)
    print('Locations: ', locations)

def outMove():
    moveID = int(input("Enter Move ID: "))
    myMove = Move('move', moveID)
    name = myMove.getItemName()
    flavorText = myMove.getFlavorText()
    accuracy = myMove.getAccuracy()
    effectChance = myMove.getEffectChance()
    PP = myMove.getPP()
    priority = myMove.getPriority()
    power = myMove.getPower()
    dmgClass = myMove.getDmgClass()
    target = myMove.getTarget()
    statChanges = myMove.getStatChanges()
    moveType = myMove.getType()

    print('Name: ', name)
    print('Flavor Text: ', flavorText)
    print('Stat Changes: ', statChanges)
    print('Accuracy: ', accuracy)
    print('Effect Chance: ', effectChance)
    print('PP: ', PP)
    print('Priority: ', priority)
    print('Power: ', power)
    print('Damage Class: ', dmgClass)
    print('Target: ', target)
    print('Type: ', moveType)

def outAbility():
    abilID = int(input("Enter Ability ID: "))
    myAbil = Ability('ability', abilID)
    name = myAbil.getItemName()
    flavorText = myAbil.getFlavorText()

    print('Name: ', name)
    print('Flavor Text: ', flavorText)

def main():
    menu()


#--------------------------------------------#
main()