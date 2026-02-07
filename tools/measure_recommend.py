import time
import sys
import os

# ensure TheUniversalPokedex is on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import TUPteamrater

team = [
    {'dexNum': 1, 'name': 'bulbasaur', 'type1': 'grass', 'type2': 'poison', 'moves': []},
]

start = time.time()
res = TUPteamrater.getRecommendedMons(team, chosenGen='1', limit=3)
end = time.time()
print('Duration:', end-start)
print('Result:', res)
