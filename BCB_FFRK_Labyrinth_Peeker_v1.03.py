import os
from json import loads, dump
from re import findall, split
from time import strftime
from traceback import format_exc

# User Variables (True/False) (Case Sensitive)
# Shows fight names and elemental data
peek_at_fights = True
# Clears old fight/treasure data when new data comes in
flush_old_data = True

# Script Variables, don't edit these!
case_map = {
    '/dff/event/labyrinth/4500/select_painting': 'ParseTheData',
    '/dff/event/labyrinth/4500/choose_explore_painting': 'ParseTheData',
    '/dff/event/labyrinth/4500/get_display_paintings': 'ParseTheData'
}
treasure_pool_map = {
    '1': '5* Orbs | 5* Motes',
    '2': '6* Crystals | Rosetta Stone of Wisdom | Rainbow Crystals',
    '3': '6* Motes | 4* Rat Tails | Magic Key | Treasure Map | Lethe Potion',
    '4': 'Anima Lenses Lvl/2/3/EX | 2x Treasure Maps | Teleport Stone | Bookmark | 5* Rat Tails',
    '5': '███████████████████████\n█████HERO ARTIFACT█████\n███████████████████████'
}
element_map = {
    0: 'Fire', 1: 'Ice', 2: 'Lightning', 3: 'Earth', 4: 'Wind', 5: 'Water', 6: 'Holy', 7: 'Dark', 8: 'Poison'
}

# Initial Load
if peek_at_fights:
    print('Waiting for Labyrinth Paintings...')
else:
    print('Waiting for Labyrinth Chests...')

# Runs whenever data passes though the proxy
def response(flow):
    if flow.request.path not in case_map.keys():
        return
    data = loads(flow.response.content.decode('utf-8-sig'))
    if case_map[flow.request.path] == 'ParseTheData':
        with open('data.json', 'w', encoding='utf-8') as f:
            dump(data, f, ensure_ascii=False, indent=4)
        if flush_old_data:
            cls()
        parseTreasure(data)
        if peek_at_fights:
            parseFights(data)


def parseTreasure(data):
    try:
        left_chest_id = data['labyrinth_dungeon_session']['treasure_chest_ids'][0]
        center_chest_id = data['labyrinth_dungeon_session']['treasure_chest_ids'][1]
        right_chest_id = data['labyrinth_dungeon_session']['treasure_chest_ids'][2]
        left_chest = treasure_pool_map[str(left_chest_id)[:1]]
        center_chest = treasure_pool_map[str(center_chest_id)[:1]]
        right_chest = treasure_pool_map[str(right_chest_id)[:1]]
        print('#####################################\n#########' + strftime('%Y-%m-%d %H:%M:%S') + '#########\n#####################################')
        print('Left Chest:\n' + str(left_chest))
        print('\nCenter Chest:\n' + str(center_chest))
        print('\nRight Chest:\n' + str(right_chest))
    except:
        # print(format_exc())
        pass


def parseFights(data):
    left_elemental_info = center_elemental_info = right_elemental_info = ''
    try:
        exceptioncatcher = data['labyrinth_dungeon_session']['current_painting_status']
        if data['labyrinth_dungeon_session']['current_painting_status'] == 3:
            try:
                forced_fight = data['labyrinth_dungeon_session']['dungeon']['captures'][0]['tip_battle']['title']
                forced_info = data['labyrinth_dungeon_session']['dungeon']['captures'][0]['tip_battle']['html_content']
                forced_elemental_info = parse_elemental_info(forced_info)
                print('\n#####################################\n#########' + strftime('%Y-%m-%d %H:%M:%S') + '#########\n#####################################\nFORCED FIGHT: ' + str(forced_fight[:-12]) + '\n              ' + str(forced_elemental_info).replace(',', '\n              ') + '\n')
            except:
                # print(format_exc())
                pass
            return
        try:
            left_fight = data['labyrinth_dungeon_session']['display_paintings'][0]['dungeon']['captures'][0]['tip_battle']['title']
            left_info = data['labyrinth_dungeon_session']['display_paintings'][0]['dungeon']['captures'][0]['tip_battle']['html_content']
            left_elemental_info = parse_elemental_info(left_info)
        except Exception:
            left_fight = None
        try:
            center_fight = data['labyrinth_dungeon_session']['display_paintings'][1]['dungeon']['captures'][0]['tip_battle']['title']
            center_info = data['labyrinth_dungeon_session']['display_paintings'][1]['dungeon']['captures'][0]['tip_battle']['html_content']
            center_elemental_info = parse_elemental_info(center_info)
        except Exception:
            center_fight = None
        try:
            right_fight = data['labyrinth_dungeon_session']['display_paintings'][2]['dungeon']['captures'][0]['tip_battle']['title']
            right_info = data['labyrinth_dungeon_session']['display_paintings'][2]['dungeon']['captures'][0]['tip_battle']['html_content']
            right_elemental_info = parse_elemental_info(right_info)
        except Exception:
            right_fight = None
        if any([left_fight, center_fight, right_fight]):
            print('\n#####################################\n#########' + strftime('%Y-%m-%d %H:%M:%S') + '#########\n#####################################')
        if left_fight is not None:
            print('Left Painting:   ' + str(left_fight[:-12]) + '\n                 ' + str(left_elemental_info).replace(',', '\n                 ') + '\n')
        if center_fight is not None:
            print('Center Painting: ' + str(center_fight[:-12]) + '\n                 ' + str(center_elemental_info).replace(',', '\n                 ') + '\n')
        if right_fight is not None:
            print('Right Painting:  ' + str(right_fight[:-12]) + '\n                 ' + str(right_elemental_info).replace(',', '\n                 ') + '\n')
    except:
        # print(format_exc())
        pass


def parse_elemental_info(raw_elemental_info):
    try:
        raw_info_split = findall('(?s:<div class="p-icon-[fire|ice|thunder|soil|wind|water|holy|darkness|poison].+?<div class="p-text-.+? img-rep mlr-a mt-6"></div>)', raw_elemental_info)
        phase_info_split = findall('(?:<div class="s-tip-battle-title mb-b4">.+?</div>)', raw_elemental_info)
        for count, elem in enumerate(phase_info_split):
            phase_info_split[count] = elem.replace('<div class="s-tip-battle-title mb-b4">', '')
            phase_info_split[count] = phase_info_split[count].replace('</div>', '')
        phase_info_parsed = []
        for elem in phase_info_split:
            if len(elem) >= 4:
                phase_info_parsed.append(elem.replace('\\', ''))
        processed_elemental_info = dict()
        processed_elemental_info1 = ''
        processed_elemental_info2 = ''
        processed_elemental_info3 = ''
        for count, elem in enumerate(raw_info_split):
            if elem.find('text-weak') > 0 and count <= 8:
                if processed_elemental_info1 != '':
                    processed_elemental_info1 += ' | '
                processed_elemental_info1 += element_map[count] + ' Weak'
            elif elem.find('text-void') > 0 and count <= 8:
                if processed_elemental_info1 != '':
                    processed_elemental_info1 += ' | '
                processed_elemental_info1 += element_map[count] + ' Immune'
            elif elem.find('text-absorption') > 0 and count <= 8:
                if processed_elemental_info1 != '':
                    processed_elemental_info1 += ' | '
                processed_elemental_info1 += element_map[count] + ' Absorb'
            elif elem.find('text-half') > 0 and count <= 8:
                if processed_elemental_info1 != '':
                    processed_elemental_info1 += ' | '
                processed_elemental_info1 += element_map[count] + ' Resist'
            if processed_elemental_info1 == 'Fire Resist | Ice Resist | Lightning Resist | Earth Resist | Wind Resist | Water Resist | Holy Resist | Dark Resist | Poison Resist':
                processed_elemental_info1 = 'Resists All Elements'
            if processed_elemental_info1 == 'Fire Weak | Ice Weak | Lightning Weak | Earth Weak | Wind Weak | Water Weak | Holy Weak | Dark Weak | Poison Weak':
                processed_elemental_info1 = 'Weak To All Elements'
            if processed_elemental_info1 == 'Fire Immune | Ice Immune | Lightning Immune | Earth Immune | Wind Immune | Water Immune | Holy Immune | Dark Immune | Poison Immune':
                processed_elemental_info1 = 'Immune To All Elements'
            if processed_elemental_info1 == 'Fire Absorb | Ice Absorb | Lightning Absorb | Earth Absorb | Wind Absorb | Water Absorb | Holy Absorb | Dark Absorb | Poison Absorb':
                processed_elemental_info1 = 'Absorbs All Elements'
            if count == 8:
                processed_elemental_info[phase_info_parsed[0]] = processed_elemental_info1
            if elem.find('text-weak') > 0 and 8 < count <= 17:
                if processed_elemental_info2 != '':
                    processed_elemental_info2 += ' | '
                processed_elemental_info2 += element_map[count - 9] + ' Weak'
            elif elem.find('text-void') > 0 and 8 < count <= 17:
                if processed_elemental_info2 != '':
                    processed_elemental_info2 += ' | '
                processed_elemental_info2 += element_map[count - 9] + ' Immune'
            elif elem.find('text-absorption') > 0 and 8 < count <= 17:
                if processed_elemental_info2 != '':
                    processed_elemental_info2 += ' | '
                processed_elemental_info2 += element_map[count - 9] + ' Absorb'
            elif elem.find('text-half') > 0 and 8 < count <= 17:
                if processed_elemental_info2 != '':
                    processed_elemental_info2 += ' | '
                processed_elemental_info2 += element_map[count - 9] + ' Resist'
            if processed_elemental_info2 == 'Fire Resist | Ice Resist | Lightning Resist | Earth Resist | Wind Resist | Water Resist | Holy Resist | Dark Resist | Poison Resist':
                processed_elemental_info2 = 'Resists All Elements'
            if processed_elemental_info2 == 'Fire Weak | Ice Weak | Lightning Weak | Earth Weak | Wind Weak | Water Weak | Holy Weak | Dark Weak | Poison Weak':
                processed_elemental_info2 = 'Weak To All Elements'
            if processed_elemental_info2 == 'Fire Immune | Ice Immune | Lightning Immune | Earth Immune | Wind Immune | Water Immune | Holy Immune | Dark Immune | Poison Immune':
                processed_elemental_info2 = 'Immune To All Elements'
            if processed_elemental_info2 == 'Fire Absorb | Ice Absorb | Lightning Absorb | Earth Absorb | Wind Absorb | Water Absorb | Holy Absorb | Dark Absorb | Poison Absorb':
                processed_elemental_info2 = 'Absorbs All Elements'
            if count == 17:
                processed_elemental_info[phase_info_parsed[1]] = processed_elemental_info2
            if elem.find('text-weak') > 0 and 17 < count <= 26:
                if processed_elemental_info3 != '':
                    processed_elemental_info3 += ' | '
                processed_elemental_info3 += element_map[count - 18] + ' Weak'
            elif elem.find('text-void') > 0 and 17 < count <= 26:
                if processed_elemental_info3 != '':
                    processed_elemental_info3 += ' | '
                processed_elemental_info3 += element_map[count - 18] + ' Immune'
            elif elem.find('text-absorption') > 0 and 17 < count <= 26:
                if processed_elemental_info3 != '':
                    processed_elemental_info3 += ' | '
                processed_elemental_info3 += element_map[count - 18] + ' Absorb'
            elif elem.find('text-half') > 0 and 17 < count <= 26:
                if processed_elemental_info3 != '':
                    processed_elemental_info3 += ' | '
                processed_elemental_info3 += element_map[count - 18] + ' Resist'
            if processed_elemental_info3 == 'Fire Resist | Ice Resist | Lightning Resist | Earth Resist | Wind Resist | Water Resist | Holy Resist | Dark Resist | Poison Resist':
                processed_elemental_info3 = 'Resists All Elements'
            if processed_elemental_info3 == 'Fire Weak | Ice Weak | Lightning Weak | Earth Weak | Wind Weak | Water Weak | Holy Weak | Dark Weak | Poison Weak':
                processed_elemental_info3 = 'Weak To All Elements'
            if processed_elemental_info3 == 'Fire Immune | Ice Immune | Lightning Immune | Earth Immune | Wind Immune | Water Immune | Holy Immune | Dark Immune | Poison Immune':
                processed_elemental_info3 = 'Immune To All Elements'
            if processed_elemental_info3 == 'Fire Absorb | Ice Absorb | Lightning Absorb | Earth Absorb | Wind Absorb | Water Absorb | Holy Absorb | Dark Absorb | Poison Absorb':
                processed_elemental_info3 = 'Absorbs All Elements'
            if count == 26:
                processed_elemental_info[phase_info_parsed[2]] = processed_elemental_info3
        return processed_elemental_info
    except:
        # print(format_exc())
        pass


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
