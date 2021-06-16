from json import loads, dumps
from time import time, strftime
from re import findall
from math import floor

print('Waiting for Labyrinth Chests...')

poolmap = {'1':'5* Orbs | 5* Motes','2':'6* Crystals | Rosetta Stone of Wisdom | Rainbow Crystals','3':'6* Motes | 4* Rat Tails | Magic Key | Treasure Map | Lethe Potion','4':'Anima Lenses Lvl/2/3/EX | 2x Treasure Maps | Teleport Stone | Bookmark | 5* Rat Tails','5':'███████████████████████\n█████HERO ARTIFACT█████\n███████████████████████'}

def response(flow):

    case = '/dff/event/labyrinth/4500/'
    
    if case not in flow.request.path:
        return
    data = loads(flow.response.content.decode('utf-8-sig'))
    try:
        left_chest_id = data['labyrinth_dungeon_session']['treasure_chest_ids'][0]
        center_chest_id = data['labyrinth_dungeon_session']['treasure_chest_ids'][1]
        right_chest_id = data['labyrinth_dungeon_session']['treasure_chest_ids'][2]
        left_chest=poolmap[str(left_chest_id)[:1]]
        center_chest=poolmap[str(center_chest_id)[:1]]
        right_chest=poolmap[str(right_chest_id)[:1]]
        print('#####################################')
        print('#########'+strftime('%Y-%m-%d %H:%M:%S')+'#########')
        print('#####################################')
        print('Left Chest:\n'+str(left_chest))
        print('\nCenter Chest:\n'+str(center_chest))
        print('\nRight Chest:\n'+str(right_chest))
        print('\n\n')
    except Exception:
        pass
