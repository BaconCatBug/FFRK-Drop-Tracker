import json
import time
import re

def response(flow):
    if len(re.findall('/get_battle_init_data', flow.request.path)) == 0:
        return

    data   = json.loads(flow.response.content.decode('utf-8-sig'))
    rounds = data['battle']['rounds']

    results = {
        'materias': [],
        'potions':  [],
        'drops':    {}
    }

    for round in rounds:
        for enemy_set in round['enemy']:
            for enemy in enemy_set['children']:
                for item in enemy['drop_item_list']:
                    item_id = item['item_id'] if ('item_id' in item) else '0'
                    amount  = item['num'] if ('num' in item) else item['amount']

                    if (item_id not in results['drops'].keys()):
                        results['drops'][item_id] = {
                            'type':   item['type'],
                            'amount': 0
                        }

                    results['drops'][item_id]['amount'] += int(amount)

        for potion in round['drop_item_list']:
            results['potions'].append({
                'type':  potion['type'],
                'round': potion['round']
            })

        for materia in round['drop_materias']:
            results['materias'].append(materia['name'])

    print('######################################')
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    print('-------------------\n')

    multi_segment = False

    if len(results['drops']):
        with open('ffrk_drop_tracker_db_do_not_delete.csv') as f:
            lines    = f.read().splitlines()[1:]
            drop_ids = {x.split(',')[0]: x.split(',')[1] for x in lines}

        if (multi_segment):
            print('\n-------------------\n')

        multi_segment = True

        print('Drops:\n')

        for drop in sorted(results['drops']):
            if (drop in drop_ids.keys()):
                name = drop_ids[drop]

            elif (int(drop) in range(21000000, 24000000)):
                name = 'Relic {0}'.format(drop)

            else:
                name = 'Unknown {0} (type {1})'.format(drop, results['drops'][drop]['type'])

            amount = ': {0}'.format(results['drops'][drop]['amount'])

            print('{0}{1}'.format(name, amount))

    if len(results['potions']):
        potion_types = {
            '21': 'Blue Potion',
            '22': 'Green Potion',
            '23': 'Purple Potion',
            '31': 'Ether',
            '32': 'Orange Ether'
        }

        if (multi_segment):
            print('\n-------------------\n')

        multi_segment = True

        print('Potions:\n')

        for potion in results['potions']:
            print('Round {0}: {1}'.format(potion['round'], potion_types[potion['type']]))

    if len(results['materias']):
        if (multi_segment):
            print('\n-------------------\n')

        multi_segment = True

        print('Record Materias:\n')

        for materia in results['materias']:
            print(materia)

    print('\n\n')
    
    get_EXP_RM_Boosts(data)

    
def get_EXP_RM_Boosts(data):
    
    results = []
    
    # Alternative character names, defined by id ("buddy_id"). Workaround for characters with the same ingame name, e.g. "Cid".
    names_fixed = {
        '10000200': 'Tyro',
        '10400100': 'Dark Cecil',
        '10400200': 'Paladin Cecil',
        '10401500': 'Cid (IV)',
        '10701100': 'Cid (VII)',
        '11400800': 'Cid (XIV)'
    }
    
    buddies = data['battle']['buddy']
    buddies.sort(key=lambda x: x['pos_id'], reverse=False) # Sorting the character list by party order (top to bottom). Inherited order seems random.
    
    for buddy in buddies:
        uid = str(buddy['uid'])
        exp_boost = int(data['battle']['buddy_boost_map']['exp'][uid])
        if exp_boost!=0:
            id = str(buddy['id'])
            name = str(names_fixed[id]) if (id in names_fixed) else str(buddy['params'][0]['disp_name']) # Use the alternative name from the 'names_fixed' array if it was defined. Otherwise use the default name.
            results.append(' x{1:0.2f} {0}'.format(name, float(exp_boost)/100))
            
    if len(results):
        print('EXP RM Boost:\n-------------')
        print('\n'.join(results))
        print('\n')