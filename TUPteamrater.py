#The Universal Pokédex - Team Rater

#------------------imports---------------------#
from TUPtrainers import TRAINERSBYGAME
import TUPitems

#----------------------------------------------#
ALLTYPES = ['normal','fire','water','electric','grass','ice','fighting','poison',
            'ground','flying','psychic','bug','rock','ghost','dragon',
            'dark','steel','fairy']

#formats text into displayed format
def titleName(text):
    if not text:
        return ''
    return str(text).replace('-', ' ').title()

#sorts key-value pairs
def sortPairs(i, minVal=1):
    items = [(key, value) for key, value in i.items() if value >= minVal]
    items.sort(key=lambda x: (-x[1], x[0]))
    return items

#gets all type relationships
def getTypeChart():
    #could use pokeAPI to get type relationships, but coded here instead to improve performance by reducing loading times
    typeChart = {
        "normal": {"rock": 0.5, "ghost": 0.0, "steel": 0.5},
        "fire": {"fire": 0.5, "water": 0.5, "grass": 2.0, "ice": 2.0, "bug": 2.0, "rock": 0.5, "dragon": 0.5, "steel": 2.0},
        "water": {"fire": 2.0, "water": 0.5, "grass": 0.5, "ground": 2.0, "rock": 2.0, "dragon": 0.5},
        "electric": {"water": 2.0, "electric": 0.5, "grass": 0.5, "ground": 0.0, "flying": 2.0, "dragon": 0.5},
        "grass": {"fire": 0.5, "water": 2.0, "grass": 0.5, "poison": 0.5, "ground": 2.0, "flying": 0.5, "bug": 0.5, "rock": 2.0, "dragon": 0.5, "steel": 0.5},
        "ice": {"fire": 0.5, "water": 0.5, "grass": 2.0, "ice": 0.5, "ground": 2.0, "flying": 2.0, "dragon": 2.0, "steel": 0.5},
        "fighting": {"normal": 2.0, "ice": 2.0, "rock": 2.0, "dark": 2.0, "steel": 2.0, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "ghost": 0.0, "fairy": 0.5},
        "poison": {"grass": 2.0, "fairy": 2.0, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0.0},
        "ground": {"fire": 2.0, "electric": 2.0, "grass": 0.5, "poison": 2.0, "flying": 0.0, "bug": 0.5, "rock": 2.0, "steel": 2.0},
        "flying": {"grass": 2.0, "fighting": 2.0, "bug": 2.0, "electric": 0.5, "rock": 0.5, "steel": 0.5},
        "psychic": {"fighting": 2.0, "poison": 2.0, "psychic": 0.5, "steel": 0.5, "dark": 0.0},
        "bug": {"grass": 2.0, "psychic": 2.0, "dark": 2.0, "fire": 0.5, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "ghost": 0.5, "steel": 0.5, "fairy": 0.5},
        "rock": {"fire": 2.0, "ice": 2.0, "flying": 2.0, "bug": 2.0, "fighting": 0.5, "ground": 0.5, "steel": 0.5},
        "ghost": {"psychic": 2.0, "ghost": 2.0, "dark": 0.5, "normal": 0.0},
        "dragon": {"dragon": 2.0, "steel": 0.5, "fairy": 0.0},
        "dark": {"psychic": 2.0, "ghost": 2.0, "fighting": 0.5, "dark": 0.5, "fairy": 0.5},
        "steel": {"ice": 2.0, "rock": 2.0, "fairy": 2.0, "fire": 0.5, "water": 0.5, "electric": 0.5, "steel": 0.5},
        "fairy": {"fighting": 2.0, "dragon": 2.0, "dark": 2.0, "fire": 0.5, "poison": 0.5, "steel": 0.5}
        }
    return typeChart

#formats type text
def normaliseType(t):
    if t in (-1, None, '', 'none'):
        return None
    return str(t).strip().lower()

#gets damage mult from type relationship
def getTypeMultiplier(attackType, defendType):
    attackType = normaliseType(attackType)
    defendType = normaliseType(defendType)

    if not attackType or not defendType:
        return 1.0
    
    chart = getTypeChart()
    return chart.get(attackType, {}).get(defendType, 1.0)

#gets total damage mult
def getDamageTakenMult(attackType, defendType1, defendType2):
    mult1 = getTypeMultiplier(attackType, defendType1)
    if defendType2:
        mult2 = getTypeMultiplier(attackType, defendType2)
    else:
        mult2 = 1.0
    return mult1*mult2

#analyses inputted teams offensive and defensive type relationships, returning dictionary of statistics
def getTeamAnalysisStats(teamSlots, moveTypeLookup=None):
    mons = [mon for mon in teamSlots if mon]
    if not mons:
        return {'weak': {}, 'resist': {}, 'immune': {}, 'coverage': {}, 'teamSize': 0}
    
    weak = {}
    resist = {}
    immune = {}
    coverage = {}
    typeCounts= {}

    for mon in mons:
        type1 = normaliseType(mon.get('type1'))
        type2 = normaliseType(mon.get('type2'))
        

        if type1:
            typeCounts[type1] = typeCounts.get(type1, 0) + 1
        if type2 and type2 != type1:
            typeCounts[type2] = typeCounts.get(type2, 0) + 1

        #defensive relationships
        for atk in ALLTYPES:
            mult = getDamageTakenMult(atk, type1, type2)
            if mult == 0.0:
                immune[atk] = immune.get(atk, 0) + 1
            elif mult >= 2.0:
                weak[atk] = weak.get(atk, 0) + 1
            elif mult <= 0.5:
                resist[atk] = resist.get(atk, 0) + 1

        #offensive coverage, use moves if provided, otherwise just use types
        attackTypes = set()

        if moveTypeLookup is not None:
            for moveName in (mon.get('moves') or []):
                moveType = normaliseType(moveTypeLookup(moveName))
                if moveType:
                    attackTypes.add(moveType)
        
        if not attackTypes:
            if type1:
                attackTypes.add(type1)
            if type2 and type2 != type1:
                attackTypes.add(type2)
        
        for defend in ALLTYPES:
            best = 1.0
            for atk in attackTypes:
                best = max(best, getTypeMultiplier(atk, defend))
            if best >= 2.0:
                coverage[defend] = coverage.get(defend, 0) + 1

    return {'typeCounts': typeCounts, 'weak': weak, 'resist': resist, 'immune': immune, 'coverage': coverage, 'teamSize': len(mons)}

#gets the types of each move
def getMonMoveTypes(mon, moveTypeLookup):
    attackTypes = set()
    if moveTypeLookup is not None:
        for moveName in (mon.get('moves') or []):
            moveType = normaliseType(moveTypeLookup(moveName))
            if moveType:
                attackTypes.add(moveType)
    
    if not attackTypes:
        type1 = normaliseType(mon.get('type1'))
        type2 = normaliseType(mon.get('type2'))
        if type1:
            attackTypes.add(type1)
        if type2 and type2 != type1:
            attackTypes.add(type2)
    return attackTypes

#scores teams relationship with chosen games key trainer battles
def scoreTrainerType(typeList, mons, moveTypeLookup):
    #mixed teams skip scoring
    if not typeList or 'mixed' in typeList:
        return {'coverageMons': 0, 'weakMons': 0, 'note': 'Mixed Team'}
    
    coverageMons = 0
    weakMons = 0

    for mon in mons:
        defType1 = normaliseType(mon.get('type1'))
        defType2 = normaliseType(mon.get('type2'))
        atkTypes = getMonMoveTypes(mon, moveTypeLookup)

        #can mon hit for any trainer type for super effective
        super = False
        for trainerType in typeList:
            trainerType = normaliseType(trainerType)
            best = 1.0

            for atk in atkTypes:
                best = max(best, getTypeMultiplier(atk, trainerType))

            if best >= 2.0:
                super = True
                break
        
        if super:
            coverageMons += 1
        
        #is mon weak to any trainer type
        isWeak = False
        for trainerType in typeList:
            trainerType = normaliseType(trainerType)
            mult = getDamageTakenMult(trainerType, defType1, defType2)

            if mult >= 2.0:
                isWeak = True
                break
        
        if isWeak:
            weakMons += 1
    
    return {'coverageMons': coverageMons, 'weakMons': weakMons, 'note': ''}

#creates and returns a report of the teams relationship with key trainer battles
def getTrainerReport(teamSlots, gameKey, moveTypeLookup=None):
    #gets trainer data for chosen game
    data = TRAINERSBYGAME.get(gameKey)
    if not data:
        return f'No trainer data available for: {titleName(gameKey)}'

    #gets user team stats
    stats = getTeamAnalysisStats(teamSlots, moveTypeLookup)
    if stats['teamSize'] == 0:
        return 'Your team is empty. Please add Pokémon first.'
    
    #only filled team slots
    mons = [mon for mon in teamSlots if mon]

    lines = []

    #gyms
    lines.append('GYM MATCHUPS:')
    for gym in data.get('gyms', []):
        name = gym.get('name', 'Gym')
        types = [normaliseType(t) for t in (gym.get('types') or []) if normaliseType(t)]

        #scores team against trainer types
        result = scoreTrainerType(types, mons, moveTypeLookup)
        if types:
            typeText = ', '.join(titleName(t) for t in types)
        else:
            typeText = 'Mixed/Unknown'
        
        lines.append(f'- {name} ({typeText})')
        if result['note']:
            lines.append(f'   - Note: {result["note"]}')
        lines.append(f'   - Coverage: {result["coverageMons"]}/{stats["teamSize"]} team members')
        lines.append(f'   - Weakness: {result["weakMons"]}/{stats["teamSize"]} team members\n')

    #elite four
    lines.append('ELITE FOUR:')
    for elite in data.get('elite_four', []):
        name = elite.get('name', 'Elite Four')
        types = [normaliseType(t) for t in (elite.get('types') or []) if normaliseType(t)]

        #scores team against trainer types
        result = scoreTrainerType(types, mons, moveTypeLookup)
        if types:
            typeText = ', '.join(titleName(t) for t in types)
        else:
            typeText = 'Mixed/Unknown'
        
        lines.append(f'- {name} ({typeText})')
        if result['note']:
            lines.append(f'   - Note: {result["note"]}')
        lines.append(f'   - Coverage: {result["coverageMons"]}/{stats["teamSize"]} team members')
        lines.append(f'   - Weakness: {result["weakMons"]}/{stats["teamSize"]} team members\n')

    return '\n'.join(lines)

#determines whether a type is strong against another
def strongAgainst(defType):
    strong = []
    for atk in ALLTYPES:
        if getTypeMultiplier(atk, defType) >= 2.0:
            strong.append(atk)
    return strong

#determines whether a type is resisted by a given type combination
def resists(atkType, defType1, defType2):
    mult = getDamageTakenMult(atkType, defType1, defType2)
    
    #return True if resists/immune otherwise False
    return mult == 0.0 or mult <= 0.5

#suggests pokemon to improve team
def getRecommendedMons(teamSlots, chosenGen, gameVersions=None, limit=10, moveTypeLookup=None):
    #step 1: find team's missing offensive coverage
    #step 2: find top weaknesses
    #step 3: set of desired types to search
    #step 4: list candidates
    #step 5: score candidates

    gen = int(chosenGen)
    stats = getTeamAnalysisStats(teamSlots, moveTypeLookup)
    if stats.get('teamSize', 0) == 0:
        return []
    
    teamDexNums = set(mon.get('dexNum') for mon in teamSlots if mon)
    teamNamesLower = set((mon.get('name') or '').strip().lower() for mon in teamSlots if mon)

    #step 1
    missingCoverage = [t for t in ALLTYPES if stats['coverage'].get(t, 0) == 0]

    #step 2
    sortedWeak = sorted(stats['weak'].items(), key=lambda x: x[1], reverse=True)
    topWeakTypes = [t for t, i in sortedWeak[:3]]

    #step 3
    desiredTypes = set()

    for t in missingCoverage[:4]:
        desiredTypes.add(t)

    for weak in topWeakTypes:
        for atk in strongAgainst(weak):
            desiredTypes.add(atk)

    #step 4
    candidates = []
    seenDex = set()

    for t in desiredTypes:
        #uses same search as in encyclopedia
        criteria = {'itemType': 'Pokémon', 'query': '', 'gen': str(gen), 'type': t}
        rows = TUPitems.searchEncyclopedia(criteria, limit=1)
        for dexNum, displayName, spriteURL in rows:
            if dexNum in teamDexNums or dexNum in seenDex:
                continue #skips to next loop
            seenDex.add(dexNum)
            candidates.append((dexNum, displayName, spriteURL))

    #step 5
    recommended = []
    for dexNum, displayName, spriteURL in candidates:
        try:
            monObj = TUPitems.Mon('mon', int(dexNum), gen)
            monName = (monObj.getItemName() or '').strip().lower()
            if monName and monName in teamNamesLower:
                continue

            type1 = normaliseType(monObj.getType1())
            type2 = normaliseType(monObj.getType2())
            bst = int(monObj.getBST())

            atkTypes = [t for t in [type1, type2] if t and t != 'none' and t != -1]

            #how many missing types can this mon hit for super effective
            coverageGain = 0
            for missing in missingCoverage:
                best = 1.0
                for atk in atkTypes:
                    best = max(best, getTypeMultiplier(atk, missing))
                if best >= 2.0:
                    coverageGain += 1
            
            #defensive score
            resistCount = 0
            weakList = []
            for weak in topWeakTypes:
                if resists(weak, type1, type2):
                    resistCount += 1
                    weakList.append(weak)
            
            #weighted scoring:
            #offense > defense > power
            score = (coverageGain*10) + (resistCount*6) + (bst/120.0)

            reasons = []
            if coverageGain > 0:
                reasons.append(f'adds coverage against {coverageGain} missing types')
            if resistCount > 0:
                reasons.append('resists ' + ', '.join(titleName(weak) for weak in weakList))
            if not reasons:
                reasons.append('high BST option')

            recommended.append({
                'id': int(dexNum),
                'name': displayName,
                'spriteURL': spriteURL,
                'type1': type1,
                'type2': type2,
                'bst': bst,
                'coverageGain': coverageGain,
                'resistCount': resistCount,
                'score': score,
                'reason': '; '.join(reasons)
            })
        except:
            continue
    
    recommended.sort(key=lambda i: i['score'], reverse=True)
    return recommended[:limit]


