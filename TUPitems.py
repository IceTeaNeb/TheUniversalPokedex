#The Universal Pokédex - retrieving information from PokéAPI

#-------------------imports------------------#
import pokebase as pb

#---------functions----------#
def spriteURLFromDexNum(dexNum):
    if not dexNum:
        return None
    else:
        return f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{dexNum}.png'
    
def parseIDFromURL(url):
    try:
        return int(str(url).rstrip('/').split('/')[-1])
    except:
        return None

def searchEncyclopedia(criteria, limit=200):
    itemType = criteria.get('itemType', 'Pokémon')
    query = (criteria.get('query') or '').strip().lower()
    gen = criteria.get('gen', 'Any')
    typeName = (criteria.get('type') or '').strip().lower()
    if typeName in ('', 'any', None):
        typeName = None

    #if user typed something
    if query:
        try:
            if itemType == 'Pokémon':
                if not query.isdigit():
                    p = pb.pokemon(query)
                else:
                    p = pb.pokemon(int(query))

                dexNum = int(p.id)
                name = str(p.name).replace('-', ' ').title()
                return [(dexNum, name, spriteURLFromDexNum(dexNum))]

            if itemType == 'Move':
                if not query.isdigit():
                    m = pb.move(query)
                else:
                    m = pb.move(int(query))
                moveID = int(m.id)
                name = str(m.name).replace('-', ' ').title()
                return [(moveID, name, None)]
            
            if itemType == 'Ability':
                rows = []
                if gen == 'Any':
                    try:
                        abilityList = pb.ability()
                        for entry in abilityList[:limit]:
                            abilID = parseIDFromURL(getattr(entry, 'url', None))
                            if abilID:
                                name = str(entry.name).replace('-', ' ').title()
                                rows.append((abilID, name, None))
                    except:
                        return []
                    
                    return rows
                
                g = pb.generation(int(gen))
                for i in g.abilities[:limit]:
                    abilID = parseIDFromURL(getattr(i, 'url', None))
                    if abilID:
                        rows.append((abilID, str(i.name).replace('-', ' ').title(), None))

        except:
            return []
        
    #else build filtered list
    def getFirstN(items):
        return items[:limit]
    
    #pokemon list
    if itemType == 'Pokémon':
        candidates = None

        #filter by gen
        if gen != 'Any':
            g = pb.generation(int(gen))
            genDict = {}
            for i in g.pokemon_species:
                dexNum = parseIDFromURL(getattr(i, 'url', None))
                if dexNum:
                    genDict[i.name] = dexNum
            candidates = genDict

        #filter by type
        if typeName:
            t = pb.type_(typeName)
            typeDict = {}
            for i in t.pokemon:
                p = i.pokemon
                dexNum = parseIDFromURL(getattr(p, 'url', None))
                if dexNum:
                    typeDict[p.name] = dexNum

            if candidates is None:  
                candidates = typeDict
            else:
                candidates = {name: candidates[name] for name in candidates if name in typeDict}

        if not candidates:
            return []
        
        rows = []
        for name, dexNum in getFirstN(sorted(candidates.items(), key=lambda x: x[1])):
            rows.append((dexNum, str(name).replace('-', ' ').title(), spriteURLFromDexNum(dexNum)))
        return rows
    
    #move list
    if itemType == 'Move':
        candidates = None

        #filter by gen
        if gen != 'Any':
            g = pb.generation(int(gen))
            genDict = {}
            for i in g.moves:
                moveID = parseIDFromURL(getattr(i, 'url', None))
                if moveID:
                    genDict[i.name] = moveID
            candidates = genDict

        #filter by type
        if typeName:
            t = pb.type_(typeName)
            typeDict = {}
            for i in t.moves:
                moveID = parseIDFromURL(getattr(i, 'url', None))
                if moveID:
                    typeDict[i.name] = moveID

            if candidates is None:  
                candidates = typeDict
            else:
                candidates = {name: candidates[name] for name in candidates if name in typeDict}

        if not candidates:
            return []
        
        rows = []
        for name, moveID in getFirstN(sorted(candidates.items(), key=lambda x: x[1])):
            rows.append((moveID, str(name).replace('-', ' ').title(), None))
        return rows
    
    #ability list
    if itemType == 'Ability':
        #user must search or pick gen
        if gen == 'Any':
            return []
        
        g = pb.generation(int(gen))
        rows = []
        for i in g.abilities[:limit]:
            abilID = parseIDFromURL(getattr(i, 'url', None))
            if abilID:
                rows.append((abilID, str(i.name).replace('-', ' ').title(), None))
        return rows
    
    return []
#---------Item Class---------#
class Item:
    def __init__(self, itemGroup, id, chosenGen):

        ##---------Attributes---------##
        self._itemGroup = itemGroup
        self._id = id
        self._chosenGen = chosenGen
        
        if self._itemGroup == 'mon':    #for Mon class
            langDict = {1:1, 2:1, 3:1, 4:1, 5:1, 6:6, 7:7, 8:7, 9:0}   #gen : english index
            self._name = pb.pokemon(id).name    ##name of pokemon
            self._fromGen = pb.pokemon_species(id).generation.id    ##generation item is from
            self._flavorText = next((i.flavor_text.replace("\n", " ") for i in pb.pokemon_species(id).flavor_text_entries if getattr(i.language, "name", None) == "en"), "") ##pokemon flavor text, in english

        elif self._itemGroup == 'move': #for Move class
            langDict = {1:6, 2:6, 3:0, 4:0, 5:1, 6:6, 7:7, 8:7, 9:0}   #gen : english index
            self._name = pb.move(id).name   ##name of move
            self._fromGen = pb.move(self._name).generation.id   ##generation item is from
            self._flavorText = (pb.move(id).flavor_text_entries[langDict[self._fromGen]].flavor_text).replace("\n", " ")    ##move flavor text

        elif self._itemGroup == 'ability':  #for Ability class
            langDict = {3:1, 4:1, 5:1, 6:6, 7:7, 8:7, 9:1}   #gen : english index
            self._name = pb.ability(id).name    ##name of ability
            self._fromGen = pb.ability(self._name).generation.id    ##generation item is from
            self._flavorText = (pb.ability(id).flavor_text_entries[langDict[self._fromGen]].flavor_text).replace("\n", " ") ##ability flavor text
            
    ##---------Methods---------#
    ##getter methods
    def getItemGroup(self):
        return self._itemGroup
    def getItemName(self):
        return self._name
    def getItemID(self):
        return self._id
    def getItemChosenGen(self):
        return self._chosenGen
    def getItemFromGen(self):
        return self._fromGen
    def getFlavorText(self):
        return self._flavorText

#---------Ability Class---------#
class Ability(Item):
    def __init__(self, itemGroup, id, chosenGen):
        super().__init__(itemGroup, id, chosenGen)

#---------Move Class---------#
class Move(Item):
    def __init__(self, itemGroup, id, chosenGen):

        ##---------Attributes---------##
        super().__init__(itemGroup, id, chosenGen)
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
    def __init__(self, itemGroup, idOrName, chosenGen):

        ##---------Attributes---------##
        super().__init__(itemGroup, idOrName, chosenGen)
        
        try:
            pokemon = pb.pokemon(idOrName)
            species = pb.pokemon_species(idOrName)
        except Exception:
            raise ValueError("Invalid Pokémon name or ID")

        self._dexNum = pokemon.id
        self._name = pokemon.name

        #ensures species is in english
        self._englishGenus = next((i.genus for i in species.genera if i.language.name == 'en'), None)
        self._species = self._englishGenus or 'Unknown'

        self._type1 = pokemon.types[0].type.name
        try:
            self._type2 = pokemon.types[1].type.name
        except IndexError:  ###if pokemon has only one type
            self._type2 = -1
        self._height = pokemon.height/10
        self._weight = pokemon.weight/10

        self._HP = pokemon.stats[0].base_stat
        self._Atk = pokemon.stats[1].base_stat
        self._Def = pokemon.stats[2].base_stat
        self._SpA = pokemon.stats[3].base_stat
        self._SpD = pokemon.stats[4].base_stat
        self._Spe = pokemon.stats[5].base_stat
        self._BST = self._HP+self._Atk+self._Def+self._SpA+self._SpD+self._Spe

        self._catchRate = species.capture_rate

        self._eggGroups = ''
        for i in species.egg_groups:
            self._eggGroups += str(i.name) + '|'    ###separated by |

        self._gender = species.gender_rate
        self._eggCycle = species.hatch_counter
        self._evoChainID = species.evolution_chain.id

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
            self._preEvo = species.evolves_from_species.name
        except AttributeError:  ###to show pokemon has no pre-evolution
            self._preEvo = -1

        self._locations = ''
        for i in range(len(pokemon.location_area_encounters)):
            self._locations += str(pokemon.location_area_encounters[i].location_area.name) + '|'

        self._moves = ''
        for i in range(len(pokemon.moves)):
            self._moves += str(pokemon.moves[i].move.name) + '|' ###separated by |

        self._abilities = ""
        for a in pokemon.abilities:
            self._abilities += str(a.ability.name) + "|"

        self._spriteURL = pokemon.sprites.front_default

    ##---------Methods---------##
    def getDexNum(self):
        return self._dexNum
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
    def getMoves(self):
        return self._moves
    def getAbilities(self):
        return self._abilities
    def getGender(self):
        return self._gender
    def getEggCycle(self):
        return self._eggCycle
    def getSpriteURL(self):
        return self._spriteURL


###---temporary functions for displaying Item details---###
#display option menu
def menu():
    userIn = int(input("[0]: Pokémon Details\n[1]: Move Details\n[2]: Ability Details\nEnter Option:"))
    if userIn == 0:
        outMon()
    elif userIn == 1:
        outMove()
    elif userIn == 2:
        outAbility()

#display Pokemon details
def outMon():
    monID = int(input("Enter Pokémon ID: "))
    chosenGen = int(input("Enter Generation Number: "))
    myMon = Mon('mon', monID, chosenGen)
    dexNum = myMon.getDexNum()
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
    moves = myMon.getMoves()

    #sprite = myMon.getSprite()


    print('Name: ' + name)
    print('Pokédex Number: ', dexNum)
    print('Type 1: ', type1)
    print('Type 2: ', type2)
    print('Stats [BST, HP, Atk, Def, SpA, SpD, Spe]: ', stats)
    print('Evolution Chain: ', evoList)
    print('Pre-Evolution: ', preEvo)
    print('Locations: ', locations)
    print('Moves: ', moves)

#display moves details
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

#display ability details
def outAbility():
    abilID = int(input("Enter Ability ID: "))
    myAbil = Ability('ability', abilID)
    name = myAbil.getItemName()
    flavorText = myAbil.getFlavorText()

    print('Name: ', name)
    print('Flavor Text: ', flavorText)