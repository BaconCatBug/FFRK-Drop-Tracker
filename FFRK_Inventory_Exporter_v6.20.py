# coding=utf-8

from json import dump, loads
from os import write, read, path, remove
from datetime import datetime
from time import sleep
japan = 0
ignore_crappy_core_soul_breaks = 1
ignore_three_star_and_lower_relics = 1
soul_break_export_level = 2
only_export_level_99_magicite = 1
export_raw_json = 0
modified_id_export = 1

print("Enter your Item Inventory, and then your Vault, to export all data.")


def response(flow):
    cases = {
        '/dff/party/list_equipment': 'inventory_relics',
        '/dff/party/list_other': 'list_other',
        '/dff/party/list_buddy?part=0&split=3': 'soul_breaks0',
        '/dff/party/list_buddy?part=1&split=3': 'soul_breaks1',
        '/dff/party/list_buddy?part=2&split=3': 'soul_breaks1',
        '/dff/beast/list1': 'main_magicite1',
        '/dff/beast/list2': 'main_magicite2',
        '/dff/warehouse/get_equipment_list': 'vault_relic',
        '/dff/warehouse/get_record_materia_list': 'vault_rm',
        '/dff/warehouse/get_beast_list': 'vault_magicite',
        '/dff/equipment_reference/equipment_references?type=GET': 'equip_collection'
    }

    if flow.request.path not in cases.keys():
        return

    data = loads(flow.response.content.decode('utf-8-sig'))

    if cases[flow.request.path] == 'inventory_relics':
        getRelics(data['equipments'], '1-FFRK-Inventory-Relics')
        if export_raw_json == 1:
            exportRawJson(data, 'list_equipment')

    elif cases[flow.request.path] == 'main_magicite1':
        getMagicite(data['beasts'], '5-FFRK-Magicite1')
        if export_raw_json == 1:
            exportRawJson(data, 'list1')
            
    elif cases[flow.request.path] == 'main_magicite2':
        getMagicite2(data['beasts'], '5-FFRK-Magicite2')
        if export_raw_json == 1:
            exportRawJson(data, 'list2')

    elif cases[flow.request.path] == 'vault_relic':
        getRelics(data['equipments'], '2-FFRK-Vault-Relics')
        if export_raw_json == 1:
            exportRawJson(data, 'get_equipment_list')

    elif cases[flow.request.path] == 'soul_breaks0':
        getSBs(data['soul_strikes'], '3-FFRK-Soul-Breaks',0)
        getLMs(data['legend_materias'], '7-FFRK-Legend-Materia',0)
        # getBuddies(data['buddies'], 'X-FFRK-Characters')
        if export_raw_json == 1:
            exportRawJson(data, 'list_buddy',0)
            
    elif cases[flow.request.path] == 'soul_breaks1':
        getSBs(data['soul_strikes'], '3-FFRK-Soul-Breaks',1)
        getLMs(data['legend_materias'], '7-FFRK-Legend-Materia',1)
        # getBuddies(data['buddies'], 'X-FFRK-Characters')
        if export_raw_json == 1:
            exportRawJson(data, 'list_buddy',1)

    elif cases[flow.request.path] == 'list_other':
        getAbilities(data['abilities'], '4-FFRK-Abilities')
        getOrbs(data['materials'], '6-FFRK-Orbs')
        # getRMs(data['record_materias'], 'X-FFRK-Inventory-Record-Materia')
        if export_raw_json == 1:
            exportRawJson(data, 'list_other')

    elif cases[flow.request.path] == 'equip_collection':
        pass
        # getEquipHistory(data['equipment_references'], 'X-FFRK-Equipment-Collection')
    if export_raw_json == 1:
        exportRawJson(data, 'equip_collection')

    elif cases[flow.request.path] == 'vault_rm':
        pass
        # getRMs(data['record_materias'], 'X-FFRK-Vault-Record-Materia')
    if export_raw_json == 1:
        exportRawJson(data, 'get_record_materia_list')

    elif cases[flow.request.path] == 'vault_magicite':
        pass
        # getVaultMagicite(data['beasts'], 'X-FFRK-Vault-Magicite')
    if export_raw_json == 1:
        exportRawJson(data, 'get_beast_list')

def getRelics(data, filename):
    elems = []

    for elem in data:
        relic_id = elem['equipment_id']
        name = elem['name'].replace(u'＋', '+')
        base_rarity = elem['base_rarity']
        rarity = elem['rarity']
        realm_id = int(str(elem['series_id'])[1:3]) if elem['series_id'] > 10 else 99
        if modified_id_export == 1 and elem['rarity'] < 101:
            if (rarity - base_rarity) == 1:
                relic_id = relic_id*10 + 1
            elif (rarity - base_rarity) == 2:
                relic_id = relic_id*10 + 2
            elif (rarity - base_rarity) == 3:
                relic_id = relic_id*10 + 3
            else:
                relic_id = relic_id*10
        
        if modified_id_export == 1 and elem['rarity'] == 101:
            if (name.endswith(')+++')):
                relic_id = relic_id*10 + 3
                rarity += 3
            elif (name.endswith(')++')):
                relic_id = relic_id*10 + 2
                rarity += 2
            elif (name.endswith(')+')):
                relic_id = relic_id*10 + 1
                rarity += 1
            else:
                relic_id = relic_id*10
        rosetta_param = elem['hammering_affect_param_key']
        rosetta_value = elem['hammering_num']
        rosetta_atk = rosetta_def = rosetta_matk = rosetta_mdef = rosetta_mnd = 0
        if rosetta_param == 'atk':
            rosetta_atk = rosetta_value
        elif rosetta_param == 'def':
            rosetta_def = rosetta_value
        elif rosetta_param == 'matk':
            rosetta_matk = rosetta_value
        elif rosetta_param == 'mdef':
            rosetta_mdef = rosetta_value
        elif rosetta_param == 'mnd':
            rosetta_mnd = rosetta_value
        inherit_effect = ''
        if elem['rarity'] == 101:
            inherit_effect = elem['buddy_sacred_equipment_materias'][0]['record_materia']['name']

        elems.append(
            [relic_id, name, base_rarity, rarity, realm_id, rosetta_atk, rosetta_def, rosetta_matk, rosetta_mdef,
             rosetta_mnd, inherit_effect])

    elems = sorted(elems, key=lambda x: (x[0], -x[3], x[4], x[1]))

    with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
        f.write('\ufeff')
        f.write('#ID, Item, Base Rarity, Rarity, Realm, A.Atk, A.Def, A.Mag, A.Res, A.Mnd, Inherit Effect\n')

        for elem in elems:
            if ignore_three_star_and_lower_relics == 1:
                if elem[3] > 3:
                    f.write(
                        '"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3],
                                                                                     elem[4], elem[5], elem[6], elem[7],
                                                                                     elem[8], elem[9], elem[10]))
            else:
                f.write('"{}","{}","{}, {}","{}","{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3],
                                                                                    elem[4], elem[5], elem[6], elem[7],
                                                                                    elem[8], elem[9], elem[10]))

def getRMs(data, filename):
    elems = []

    for elem in data:
        rm_id = elem['record_materia_id']
        name = elem['name']
        elems.append([rm_id, name])

    elems = sorted(elems, key=lambda x: (x[0], x[1]))

    with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
        f.write('\ufeff')
        f.write('#ID, RM\n')

        for elem in elems:
            f.write('"{}","{}"\n'.format(elem[0], elem[1]))

def getAbilities(data, filename):
    elems = []

    for elem in data:
        abil_id = elem['ability_id']
        name = elem['name']
        category_id = elem['category_id']
        category_name = elem['category_name']
        rarity = elem['rarity']
        rank = elem['grade']

        if abil_id != 30131091:
            elems.append([abil_id, name, category_name, rarity, rank, category_id])

    elems = sorted(elems, key=lambda x: (x[0], -x[3], x[5], x[1]))

    with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
        f.write('\ufeff')
        f.write('#ID, Ability, Category_Name, Rarity, Rank, Category_ID\n')

        for elem in elems:
            f.write('"{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))

def getOrbs(data, filename):
    elems = []

    for elem in data:
        orb_id = elem['id']
        name = elem['name']
        rarity = elem['rarity']
        amount = elem['num']

        if (
                orb_id <= 40000078 and orb_id != 40000069 and orb_id != 40000020 and orb_id != 40000019 and orb_id != 40000018 and orb_id != 40000017 and orb_id != 40000016):
            elems.append([orb_id, name, rarity, amount])

    elems = sorted(elems, key=lambda x: (-x[2]))

    with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
        f.write('\ufeff')
        f.write('#ID, Orb, Rarity, Amount\n')

        for elem in elems:
            f.write('"{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3]))

def getSBs(data, filename, n):
    teir = {0: '???', 1: 'Default', 2: 'Shared', 3: 'Unique', 4: 'Super', 5: 'Burst', 6: 'Overstrike', 7: 'Ultra',
            8: 'Chain', 9: 'Arcane Overstrike', 10: 'Glint', 11: 'Awakening', 12: 'Syncro', 13: 'Limit Break Overstrike', 14: 'Limit Break Glint', 15: '???', 16: '???', 17: '???'}
    elems = []

    for elem in data:
        sb_id = elem['id']
        name = elem['name']
        char_id = elem['allowed_buddy_id']
        char = elem['allowed_buddy_name'] if 'allowed_buddy_name' in elem.keys() else None
        category_id = elem['soul_strike_category_id']
        if japan != 1:
            category = teir[elem['soul_strike_category_id']]
        else:
            category = elem['soul_strike_category_name'].title()

        if ignore_crappy_core_soul_breaks == 1:
            if (category_id >= soul_break_export_level) and (
                    char_id == 10000200 or char_id >= 10004000 or char_id == 0):
                elems.append([sb_id, name, char_id, char, category_id, category])
        else:
            if (category_id >= soul_break_export_level) and (char_id >= 10000000 or char_id == 0):
                elems.append([sb_id, name, char_id, char, category_id, category])

    elems = sorted(elems, key=lambda x: (x[0], x[2], x[4]))
    if n == 0:
        with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
            f.write('\ufeff')
            f.write('#ID, Soul Break, Character ID, Character, Type ID, Type\n')

            for elem in elems:
                f.write('"{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))
    else:
        with open('{}.csv'.format(filename), 'a', encoding="utf-8") as f:
            for elem in elems:
                f.write('"{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))

def getMagicite(data, filename):
    elems = []

    for elem in data:
        magicite_id = elem['beast_id']
        name = elem['name']
        rarity = elem['rarity']
        level = elem['level']
        max_level = elem['max_level']
        elementid = elem['elements'][0]['id']
        element = elem['elements'][0]['name']

        if level == 99 and only_export_level_99_magicite != 0:
            elems.append([magicite_id, name, rarity, level, max_level, elementid, element])
        elif only_export_level_99_magicite == 0:
            elems.append([magicite_id, name, rarity, level, max_level, elementid, element])
    elems = sorted(elems, key=lambda x: (x[0], x[1], x[5]))

    with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
        f.write('\ufeff')
        f.write('#ID, Name, Rarity, Level, Max Level, Element_id, Element')

        for elem in elems:
            f.write('\n"{}","{}","{}","{}","{}","{}","{}"'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5],
                                                                  elem[6]))
    if path.exists('5-FFRK-Magicite2.csv') and path.exists('5-FFRK-Magicite1.csv'):
        data = data2 = ""
        with open('5-FFRK-Magicite1.csv') as fp: 
            data = fp.read()
        with open('5-FFRK-Magicite2.csv') as fp: 
            data2 = fp.read()
        data += "\n"
        data += data2
        with open ('5-FFRK-Magicite.csv', 'w') as fp: 
            fp.write(data)
        remove('5-FFRK-Magicite1.csv')
        remove('5-FFRK-Magicite2.csv')

def getMagicite2(data, filename):
    elems = []

    for elem in data:
        magicite_id = elem['beast_id']
        name = elem['name']
        rarity = elem['rarity']
        level = elem['level']
        max_level = elem['max_level']
        elementid = elem['elements'][0]['id']
        element = elem['elements'][0]['name']

        if level == 99 and only_export_level_99_magicite != 0:
            elems.append([magicite_id, name, rarity, level, max_level, elementid, element])
        elif only_export_level_99_magicite == 0:
            elems.append([magicite_id, name, rarity, level, max_level, elementid, element])
    elems = sorted(elems, key=lambda x: (x[0], x[1], x[5]))

    with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
        for elem in elems:
            f.write('"{}","{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5],
                                                                  elem[6]))
    if path.exists('5-FFRK-Magicite2.csv') and path.exists('5-FFRK-Magicite1.csv'):
        data = data2 = ""
        with open('5-FFRK-Magicite1.csv') as fp: 
            data = fp.read()
        with open('5-FFRK-Magicite2.csv') as fp: 
            data2 = fp.read()
        data += "\n"
        data += data2
        with open ('5-FFRK-Magicite.csv', 'w') as fp: 
            fp.write(data)
        remove('5-FFRK-Magicite1.csv')
        remove('5-FFRK-Magicite2.csv')

def getVaultMagicite(data, filename):
    elems = []

    for elem in data:
        magicite_id = elem['beast_id']
        name = elem['name']
        rarity = elem['rarity']
        level = elem['level']

        elems.append([magicite_id, name, rarity, level])

    elems = sorted(elems, key=lambda x: (-x[3], x[0], x[1]))

    with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
        f.write('\ufeff')
        f.write('#ID, Name, Rarity, Level\n')

        for elem in elems:
            f.write('"{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3]))

def getBuddies(data, filename):
    elems = []

    for elem in data:
        buddy_id = elem['buddy_id']
        realm_id = int(str(elem['series_id'])[1:3]) if elem['series_id'] < 200000 else 99
        if realm_id == 99:
            realm = 'CORE'
        elif realm_id == 50:
            realm = 'FFT'
        elif realm_id == 60:
            realm = 'Type-0'
        elif realm_id == 70:
            realm = 'KH'
        elif realm_id == 90:
            realm = 'Beyond'
        else:
            realm = str(realm_id)

        name = elem['name']
        job = elem['job_name']
        level = elem['level']
        max_level = elem['level_max']
        s_levels = elem['sphere_skill_level']
        hp = elem['hp']
        accuracy = elem['acc']
        attack = elem['atk']
        defense = elem['def']
        magic = elem['matk']
        resistance = elem['mdef']
        mind = elem['mnd']
        speed = elem['spd']
        evasion = elem['eva']

        elems.append(
            [buddy_id, realm, name, job, level, max_level, s_levels, hp, accuracy, attack, defense, magic, resistance,
             mind,
             speed, evasion])

    elems = sorted(elems, key=lambda x: (x[0], x[2], x[1]))

    with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
        f.write('\ufeff')
        f.write(
            '#ID, Series,  Name, Job, Level, Max Level, Sphere Levels, HP, Accuracy, Attack, Defense, Magic, Resistance, Mind, Speed, Evasion\n')

        for elem in elems:
            f.write('"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"\n'.format(
                elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7], elem[8], elem[9], elem[10],
                elem[11], elem[12], elem[13], elem[14], elem[15]))


def getLMs(data, filename, n):
    elems = []

    for elem in data:
        lm_id = elem['id']
        charname = elem['buddy_name']
        name = elem['name']
        description = '"{}"'.format(elem['description'])

        elems.append([lm_id, charname, name, description])

    elems = sorted(elems, key=lambda x: (x[0], x[1], x[2]))
    if n == 0:
        with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
            f.write('\ufeff')
            f.write('#ID, Character, LM Name, Effect\n')
            for elem in elems:
                f.write('"{}","{}","{}",{}\n'.format(elem[0], elem[1], elem[2], elem[3]))
    else:
        with open('{}.csv'.format(filename), 'a', encoding="utf-8") as f:
            for elem in elems:
                f.write('"{}","{}","{}",{}\n'.format(elem[0], elem[1], elem[2], elem[3]))


def getEquipHistory(data, filename):
    elems = []

    for elem in data:
        history_id = elem['id']
        name = elem['name']
        rarity = elem['rarity']
        created_at = elem['created_at']

        date_aqu = datetime.utcfromtimestamp(float(created_at)).strftime('%Y-%m-%d %H:%M UTC')
        elems.append([history_id, name, rarity, created_at, date_aqu])

    elems = sorted(elems, key=lambda x: (x[0], x[3], x[2]))

    with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
        f.write('\ufeff')
        f.write('#ID, Name, Rarity,Acquired\n')

        for elem in elems:
            f.write('"{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[4]))


def exportRawJson(data, filename):
    with open('{}.json'.format(filename), 'w', encoding="utf-8") as json_file:
        dump(data, json_file)

