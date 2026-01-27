#The Universal Pokédex - Team Rater

#------------------imports---------------------#
from TUPtrainers import TRAINERSBYGAME

#----------------------------------------------#
ALLTYPES = ['normal','fire','water','electric','grass','ice','fighting','poison',
            'ground','flying','psychic','bug','rock','ghost','dragon',
            'dark','steel','fairy']

def titleName(text):
    if not text:
        return ''
    return str(text).replace('-', ' ').title()

def sortedPairs(i, minVal=1):
    items = [(key, value) for key, value in i.items() if value >= minVal]
    items.sort(key=lambda x: (-x[1], x[0]))
    return items

def getTypeChart():
    #could use pokeAPI to get type relationships, but hard coded instead to improve performance by reducing loading times
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

def normaliseType(t):
    if t in (-1, None, '', 'none'):
        return None
    return str(t).strip().lower()

def getTypeMultiplier(attackType, defendType):
    attackType = normaliseType(attackType)
    defendType = normaliseType(defendType)

    if not attackType or not defendType:
        return 1.0
    
    chart = getTypeChart()
    return chart.get(attackType, {}).get(defendType, 1.0)

def getDamageTakenMult(attackType, defendType1, defendType2):
    mult1 = getTypeMultiplier(attackType, defendType1)
    if defendType2:
        mult2 = getTypeMultiplier(attackType, defendType2)
    else:
        mult2 = 1.0
    return mult1*mult2

def analyseTeam(teamSlots, moveTypeLookup=None):
    stats = getTeamAnalysisStats(teamSlots, moveTypeLookup)
    if stats['teamSize'] == 0:
        return 'Your team is empty. Please add Pokémon first'
    
    weak = stats['weak']
    resist = stats['resist']
    immune = stats['immune']
    coverage = stats['coverage']
    typeCounts = stats['typeCounts']

    overlaps = sortedPairs(typeCounts, 2)
    weaknesses = sortedPairs(weak, 1)
    resistances = sortedPairs(resist, 1)
    immunities = sortedPairs(immune, 1)

    missingCoverage = [t for t in ALLTYPES if coverage.get(t, 0) == 0]
    lowCoverage = [t for t in ALLTYPES if coverage.get(t, 0) == 1]

    #create analysis report
    lines = []
    lines.append(f"Team Size: {stats['teamSize']}/6\n")

    #type overlap
    lines.append('Type Overlaps:')
    if overlaps:
        lines.extend([f' - {titleName(t)}: {count}' for t, count in overlaps])
    else:
        lines.append(" - None")
    lines.append('')

    #weaknesses
    lines.append('Team Weaknesses:')
    if weaknesses:
        lines.extend([f' - {titleName(t)}: {count}' for t, count in weaknesses])
    else:
        lines.append(" - None")
    lines.append('')

    #resistances
    lines.append('Team Resistances:')
    if resistances:
        lines.extend([f' - {titleName(t)}: {count}' for t, count in resistances])
    else:
        lines.append(" - None")
    lines.append('')

    #immunities
    lines.append('Team Immunities:')
    if immunities:
        lines.extend([f' - {titleName(t)}: {count}' for t, count in immunities])
    else:
        lines.append(" - None")
    lines.append('')

    lines.append('Offensive Coverage:')
    if missingCoverage:
        lines.append(' - No super-effective coverage for: ' + ', '.join(titleName(t) for t in missingCoverage))
    else:
        lines.append(' - You have at least one super-effective option for every type.')

    if lowCoverage:
        lines.append(' - Only one super-effective option for: ' + ', '.join(titleName(t) for t in lowCoverage))

    return '\n'.join(lines)

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

#def analyseTrainers(teamSlots, gameKey, moveTypeLookup=None):
