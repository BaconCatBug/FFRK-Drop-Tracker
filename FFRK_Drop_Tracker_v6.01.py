from json import loads
from time import time, strftime
from re import findall
from math import floor

print('Waiting for you to enter a battle...')
first_run = 0
start_time = 0


def response(flow):
    if len(findall('/get_battle_init_data', flow.request.path)) == 0:
        return
    data = loads(flow.response.content.decode('utf-8-sig'))
    rounds = data['battle']['rounds']
    results = {'materias': [], 'potions': [], 'drops': {}}
    for battle_round in rounds:
        for enemy_set in battle_round['enemy']:
            for enemy in enemy_set['children']:
                for item in enemy['drop_item_list']:
                    item_id = item['item_id'] if ('item_id' in item) else '0'
                    amount = item['num'] if ('num' in item) else item['amount']
                    if item_id not in results['drops'].keys():
                        results['drops'][item_id] = {'type': item['type'], 'amount': 0}
                    results['drops'][item_id]['amount'] += int(amount)
        for potion in battle_round['drop_item_list']:
            results['potions'].append({'type': potion['type'], 'round': potion['round']})
        for materia in battle_round['drop_materias']:
            results['materias'].append(materia['name'])
    print('######################################')
    global first_run
    global start_time
    if first_run != 0:
        seconds = floor((time() - start_time) // 1)
        minutes = floor(seconds // 60)
        seconds = seconds % 60
        m = ' minute '
        if minutes > 1 or minutes == 0:
            m = ' minutes '
        s = ' second '
        if seconds > 1 or seconds == 0:
            s = ' seconds'
    start_time = time()
    print(strftime('%Y-%m-%d %H:%M:%S'))
    if first_run != 0:
        print('Time since last battle started: ' + str(minutes) + m + 'and ' + str(seconds) + s)
    if first_run == 0:
        first_run = 1
    print('-------------------\n')
    multi_segment = False
    if len(results['drops']):
        with open('0-FFRK_Drop_Tracker_Database_Do_Not_Delete.csv')as f:
            lines = f.read().splitlines()[1:]
            drop_ids = {x.split(',')[0]: x.split(',')[1] for x in lines}
        if multi_segment:
            print('\n-------------------\n')
        multi_segment = True
        print('Drops:\n')
        for drop in sorted(results['drops']):
            if drop in drop_ids.keys():
                name = drop_ids[drop]
            elif int(drop) in range(21000000, 24000000):
                name = 'Relic {0}'.format(drop)
            else:
                name = 'Unknown (Probbaly Krakka Greens) {0} (type {1})'.format(drop, results['drops'][drop]['type'])
            amount = ': {0}'.format(results['drops'][drop]['amount'])
            print('{0}{1}'.format(name, amount))
    if len(results['potions']):
        potion_types = {'21': 'Blue Potion', '22': 'Green Potion', '23': 'Purple Potion', '31': 'Ether',
                        '32': 'Turbo Ether'}
        if multi_segment:
            print('\n-------------------\n')
        multi_segment = True
        print('Potions:\n')
        for potion in results['potions']:
            print('Round {0}: {1}'.format(potion['round'], potion_types[potion['type']]))
    if len(results['materias']):
        if multi_segment:
            print('\n-------------------\n')
        multi_segment = True
        print('Record Materias:\n')
        for materia in results['materias']:
            print(materia)
    print('\n\n')
    get_EXP_RM_Boosts(data)


def get_EXP_RM_Boosts(data):
    results = []
    names_fixed = {'10000200': 'Tyro', '10400100': 'Cecil (Dark Knight)', '10400200': 'Cecil (Paladin)',
                   '10401500': 'Cid (IV)', '10701100': 'Cid (VII)', '11400800': 'Cid (XIV)', '10500600': 'Gogo (V)',
                   '10601400': 'Gogo (VI)', '10100900': 'Theif (I)', '10002700': 'Theif (Core)'}
    buddies = data['battle']['buddy']
    buddies.sort(key=lambda x: x['pos_id'], reverse=False)
    for buddy in buddies:
        uid = str(buddy['uid'])
        exp_boost = int(data['battle']['buddy_boost_map']['exp'][uid])
        if exp_boost != 0:
            buddy_id = str(buddy['id'])
            name = str(names_fixed[buddy_id]) if (buddy_id in names_fixed) else str(buddy['params'][0]['disp_name'])
            results.append(' x{1:0.2f} {0}'.format(name, float(exp_boost) / 100))
    if len(results):
        print('EXP RM Boost:\n-------------')
        print('\n'.join(results))
        print('\n')
