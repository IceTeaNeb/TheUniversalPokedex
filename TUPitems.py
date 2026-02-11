#The Universal Pokédex - handles PokéAPI operations

#-------------------imports------------------#
import pokebase as pb
import re

#-------------------constants----------------#
BASEURL = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon'
SPRITESUBPATH = {
    1: 'versions/generation-i/red-blue/transparent',
    2: 'versions/generation-ii/crystal/transparent',
    3: 'versions/generation-iii/emerald',
    4: 'versions/generation-iv/platinum',
    5: 'versions/generation-v/black-white',
    6: 'versions/generation-vi/x-y',
    7: 'versions/generation-vii/ultra-sun-ultra-moon',
    8: 'versions/generation-viii/icons',
    9: 'versions/generation-ix/scarlet-violet',
}
TOTALSPECIESBYGEN = {
    1:151,
    2:251,
    3:386,
    4:493,
    5:649,
    6:721,
    7:809,
    8:905,
    9:1025
}

#---------functions----------#

#gets sprite URL using dexNum
def getSpriteURL(dexNum, genNum=None):
    try:
        dexNum = int(dexNum)
    except:
        return None
    
    if genNum is not None:
        try:
            genNum = int(genNum)
        except:
            genNum = None

    if genNum in SPRITESUBPATH:
        return f'{BASEURL}/{SPRITESUBPATH[genNum]}/{dexNum}.png'
    
    return f'{BASEURL}/{dexNum}.png'

#gets dexNum using URL
def getDexNumFromURL(spriteURL):
    if not spriteURL:
        return None
    
    #looks through the given url for one or more digits followed by .png
    match = re.search(r'/(\d+)\.png', str(spriteURL))

    if not match:
        return None
    return int(match.group(1))

#extracts ID from URL
def parseIDFromURL(url):
    try:
        return int(str(url).rstrip('/').split('/')[-1])
    except:
        return None

#searches pokeAPI for Pokémon, moves or abilities
def searchEncyclopedia(criteria, limit=200):
    itemType = criteria.get('itemType', 'Pokémon')
    query = (criteria.get('query') or '').strip().lower()
    gen = criteria.get('gen', 'Any')
    genNum = None
    if gen != 'Any':
        try:
            genNum = int(gen)
        except:
            genNum = None
    typeName = (criteria.get('type') or '').strip().lower()
    if typeName in ('', 'any', None):
        typeName = None

    #if user typed into search
    if query:
        try:
            #pokemon
            if itemType == 'Pokémon':
                if not query.isdigit():
                    p = pb.pokemon(query)
                else:
                    p = pb.pokemon(int(query))

                #validate gen
                if gen != 'Any':
                    fromGen = pb.pokemon_species(int(p.id)).generation.id
                    if int(gen) != int(fromGen):
                        return []
                
                #returns formatted row
                dexNum = int(p.id)
                name = str(p.name).replace('-', ' ').title()
                spriteURL = getSpriteURL(dexNum, genNum)
                return [(dexNum, name, spriteURL)]

            #move
            if itemType == 'Move':
                if not query.isdigit():
                    m = pb.move(query)
                else:
                    m = pb.move(int(query))

                #validate gen
                if gen != 'Any':
                    fromGen = m.generation.id
                    if int(gen) != int(fromGen):
                        return []

                #return formatted row
                moveID = int(m.id)
                displayName = str(m.name).replace('-', ' ').title()
                return [(moveID, displayName, None)]
            
            #ability
            if itemType == 'Ability':
                if not query.isdigit():
                    a = pb.ability(query)
                else:
                    a = pb.ability(int(query))

                if gen != 'Any':
                    fromGen = a.generation.id
                    if int(gen) != int(fromGen):
                        return []
                
                abilID = int(a.id)
                displayName = str(a.name).replace('-', ' ').title()
                return [(abilID, displayName, None)]

        except:
            return []
        
    #if no direct query, build filtered list

    #limits results to improve performance
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
                displayName = str(name).replace('-', ' ').title()
                spriteURL = getSpriteURL(dexNum, genNum)
                rows.append((dexNum, displayName, spriteURL))
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

def getTotalSpeciesUpToGen(genNum):
    try:
        genNum = int(genNum)
    except:
        return 0
    
    return TOTALSPECIESBYGEN.get(genNum, 0)

#---------Item Class---------#
#represents pokeAPI item
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
