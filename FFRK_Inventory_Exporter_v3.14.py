# coding=utf-8

import json
import os
from datetime import datetime

japan=0
ignore_crappy_core_soul_breaks=1
ignore_three_star_and_lower_relics=1
soul_break_export_level=2
only_export_level_99_magicite=0
export_raw_json=0

print("Enter your Item Inventory, and then your Vault, to export all data.")
def response(flow):
	cases = {
		'/dff/party/list_equipment': 'inventory_relics',
		'/dff/party/list_other': 'list_other',
		'/dff/party/list_buddy': 'soul_breaks',
		'/dff/beast/list': 'main_magicite',
		'/dff/warehouse/get_equipment_list': 'vault_relic',
		'/dff/warehouse/get_record_materia_list': 'vault_rm',
		'/dff/warehouse/get_beast_list': 'vault_magicite',
		'/dff/equipment_reference/equipment_references?type=GET': 'equip_collection'
	}

	if (flow.request.path not in cases.keys()):
		return

	data = json.loads(flow.response.content.decode('utf-8-sig'))

	if (cases[flow.request.path] == 'inventory_relics'):
		getRelics(data['equipments'], '1-FFRK-Inventory-Relics')
		if (export_raw_json==1):
			exportRawJson(data,'list_equipment')

	elif (cases[flow.request.path] == 'main_magicite'):
		getMagicite(data['beasts'], '5-FFRK-Magicite')
		if (export_raw_json==1):
			exportRawJson(data,'list')

	elif (cases[flow.request.path] == 'vault_relic'):
		getVaultRelics(data['equipments'], '3-FFRK-Vault-Relics')
		if (export_raw_json==1):
			exportRawJson(data,'get_equipment_list')

	elif (cases[flow.request.path] == 'soul_breaks'):
		getSBs(data['soul_strikes'], '2-FFRK-Soul_Breaks')
		getLMs(data['legend_materias'], '7-FFRK-Legend_Materia')
		#getBuddies(data['buddies'], 'X-FFRK-Characters')
		if (export_raw_json==1):
			exportRawJson(data,'list_buddy')

	elif (cases[flow.request.path] == 'list_other'):
		getAbilities(data['abilities'], '4-FFRK-Abilities')
		getOrbs(data['materials'], '6-FFRK-Orbs')
		#getRMs(data['record_materias'], 'X-FFRK-Inventory-Record_Materia')
		if (export_raw_json==1):
			exportRawJson(data,'list_other')
			
	#elif (cases[flow.request.path] == 'equip_collection'):
		#getEquipHistory(data['equipment_references'], 'X-FFRK-Equipment-Collection')
		#if (export_raw_json==1):
			#exportRawJson(data,'equip_collection')

	#elif (cases[flow.request.path] == 'vault_rm'):
		#getRMs(data['record_materias'], 'X-FFRK-Vault-Record_Materia')
		#if (export_raw_json==1):
			#exportRawJson(data,'get_record_materia_list')
		
	#elif (cases[flow.request.path] == 'vault_magicite'):
		#getVaultMagicite(data['beasts'], 'X-FFRK-Vault-Magicite')
		#if (export_raw_json==1):
			#exportRawJson(data,'get_beast_list')


def getRelics(data, filename):
	types = {
		1: 'Weapon',
		2: 'Armor',
		3: 'Accessory'
	}

	elems = []

	for elem in data:
		id			= elem['equipment_id']
		name		= elem['name'].replace(u'＋', '+')
		category	= elem['category_name']
		category_id	= elem['category_id']
		type		= types[elem['equipment_type']]
		type_id		= elem['equipment_type']
		rarity		= elem['rarity']
		realm_id	= int(str(elem['series_id'])[1:3]) if elem['series_id'] > 10 else 99

		elems.append([id, name, category, category_id, type, type_id, rarity, realm_id])

	elems = sorted(elems, key = lambda x: (-x[6], x[7], x[1]))
   
	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, Item, Category, Category_id, Type, Type_id, Rarity, Synergy\n')

		for elem in elems:
			if ignore_three_star_and_lower_relics == 1:
				if elem[6] > 3:
					f.write('"{}","{}","{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]))
			else:
				f.write('"{}","{}","{}, {}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]))

def getVaultRelics(data, filename):
	types = {
		1: 'Weapon',
		2: 'Armor',
		3: 'Accessory'
	}

	elems = []

	for elem in data:
		id			= elem['equipment_id']
		name		= elem['name'].replace(u'＋', '+')
		category	= elem['category_name']
		category_id	= elem['category_id']
		type		= types[elem['equipment_type']]
		type_id		= elem['equipment_type']
		rarity		= elem['rarity']
		realm_id	= int(str(elem['series_id'])[1:3]) if elem['series_id'] > 10 else 99

		elems.append([id, name, category, category_id, type, type_id, rarity, realm_id])

	elems = sorted(elems, key = lambda x: (-x[6], x[7], x[1]))
   
	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, Item, Category, Category_id, Type, Type_id, Rarity, Synergy\n')

		for elem in elems:
			if ignore_three_star_and_lower_relics == 1:
				if elem[6] > 3:
					f.write('"{}","{}","{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]))
			else:
				f.write('"{}","{}","{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]))


def getRMs(data, filename):
	elems = []

	for elem in data:
		id		= elem['record_materia_id']
		name	= elem['name']
		elems.append([id, name])

	elems = sorted(elems, key=lambda x: (x[1]))

	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, RM\n')

		for elem in elems:
			f.write('"{}","{}"\n'.format(elem[0], elem[1]))

def getAbilities(data, filename):
	elems = []

	for elem in data:
		id			= elem['ability_id']
		name		= elem['name']
		category_id	= elem['category_id']
		category_name	= elem['category_name']
		rarity		= elem['rarity']
		rank		= elem['grade']
		
		if (id != 30131091):
			elems.append([id, name, category_name, rarity, rank, category_id])

	elems = sorted(elems, key=lambda x: (-x[3], x[5], x[1], x[0]))

	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, Ability, Category_Name, Rarity, Rank, Category_ID\n')

		for elem in elems:
			f.write('"{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))


def getOrbs(data, filename):
	elems = []

	for elem in data:
		id		= elem['id']
		name	= elem['name']
		rarity	= elem['rarity']
		amount	= elem['num']

		if (id <= 40000078 and id != 40000069 and id != 40000020 and id != 40000019 and id != 40000018 and id != 40000017 and id != 40000016):
			elems.append([id, name, rarity, amount])

	elems = sorted(elems, key=lambda x: (-x[2], x[0]))

	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, Orb, Rarity, Amount\n')

		for elem in elems:
			f.write('"{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3]))

def getSBs(data, filename):
	teir = {
		0: '???',
		1: 'Default',
		2: 'Shared',
		3: 'Unique',
		4: 'Super',
		5: 'Burst',
		6: 'Overstrike',
		7: 'Ultra',
		8: 'Chain',
		9: 'Arcane Overstrike',
		10: 'Glint',
		11: 'Awakening',
		12: 'Syncro',
		13: '???'
	}
	elems = []

	for elem in data:
		id			= elem['id']
		name		= elem['name']
		charId		= elem['allowed_buddy_id']
		char		= elem['allowed_buddy_name'] if 'allowed_buddy_name' in elem.keys() else None
		categoryId	= elem['soul_strike_category_id']
		if japan != 1:
			category	= teir[elem['soul_strike_category_id']]
		else:
			category	= elem['soul_strike_category_name'].title() 

		if ignore_crappy_core_soul_breaks==1:
			if (categoryId >= soul_break_export_level) and (charId==10000200 or charId >= 10004000 or charId == 0):
				elems.append([id, name, charId, char, categoryId, category])
		else:	
			if (categoryId >= soul_break_export_level) and (charId >= 10000000 or charId == 0):
				elems.append([id, name, charId, char, categoryId, category])

	elems = sorted(elems, key=lambda x: (x[2], x[4], x[0]))

	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, Soul Break, Character ID, Character, Type ID, Type\n')

		for elem in elems:
			f.write('"{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))
			
def getMagicite(data, filename):
	elems = []

	for elem in data:
		id			= elem['beast_id']
		name		= elem['name']
		rarity		= elem['rarity']
		level		= elem['level']
		max_level	= elem['max_level']
		elementid	= elem['elements'][0]['id']
		element		= elem['elements'][0]['name']
		
		if level == 99 and only_export_level_99_magicite != 0:
			elems.append([id, name, rarity, level, max_level, elementid, element])
		elif only_export_level_99_magicite ==0:
			elems.append([id, name, rarity, level, max_level, elementid, element])
	elems = sorted(elems, key=lambda x: (-x[2], x[0], x[1], x[5]))

	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, Name, Rarity, Level, Max Level, Element_id, Element\n')

		for elem in elems:
			f.write('"{}","{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6]))

def getVaultMagicite(data, filename):
	elems = []

	for elem in data:
		id		= elem['beast_id']
		name	= elem['name']
		rarity	= elem['rarity']
		level	= elem['level']

		elems.append([id, name, rarity, level])

	elems = sorted(elems, key=lambda x: (-x[3], x[0], x[1]))

	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, Name, Rarity, Level\n')

		for elem in elems:
			f.write('"{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3]))

def getBuddies(data, filename):
	elems = []
    
	for elem in data:
		id          = elem['buddy_id']
		realm_id    = int(str(elem['series_id'])[1:3]) if elem['series_id'] < 200000 else 99
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

		name        = elem['name']
		job         = elem['job_name']
		level       = elem['level']
		max_level   = elem['level_max']
		s_levels    = elem['sphere_skill_level']
		hp          = elem['hp']
		accuracy    = elem['acc']
		attack      = elem['atk']
		defense     = elem['def']
		magic       = elem['matk']
		resistance  = elem['mdef']
		mind        = elem['mnd']
		speed       = elem['spd']
		evasion     = elem['eva']
        
		elems.append([id, realm, name, job, level, max_level, s_levels, hp, accuracy, attack, defense, magic, resistance, mind, speed, evasion])
    
	elems = sorted(elems, key=lambda x: (x[0], x[2], x[1]))

	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, Series,  Name, Job, Level, Max Level, Sphere Levels, HP, Accuracy, Attack, Defense, Magic, Resistance, Mind, Speed, Evasion\n')

		for elem in elems:
			f.write('"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7], elem[8], elem[9], elem[10], elem[11], elem[12], elem[13], elem[14], elem[15]))
			
			
def getLMs(data, filename):
	elems = []

	for elem in data:
		id		= elem['id']
		charname = elem['buddy_name']
		name	= elem['name']
		description = '"{}"'.format(elem['description'])
		 
		elems.append([id, charname, name, description])

	elems = sorted(elems, key=lambda x: (x[0],x[1],x[2]))

	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, Character, LM Name, Effect\n')

		for elem in elems:
			f.write('"{}","{}","{}","{}"\n'.format(elem[0], elem[1],elem[2],elem[3]))
						
def getEquipHistory(data, filename):
	elems = []

	for elem in data:
		id		= elem['id']
		name	= elem['name']
		rarity  = elem['rarity']
		created_at = elem['created_at']
		
		date_aqu = datetime.utcfromtimestamp(float(created_at)).strftime('%Y-%m-%d %H:%M UTC')
		elems.append([id, name, rarity, created_at, date_aqu])

	elems = sorted(elems, key=lambda x: (x[3],x[2],x[0]))

	with open('{}.csv'.format(filename), 'w', encoding="utf-8") as f:
		f.write('#ID, Name, Rarity,Acquired\n')

		for elem in elems:
			f.write('"{}","{}","{}","{}"\n'.format(elem[0], elem[1], elem[2],elem[4]))

def exportRawJson(data, filename):
	with open('{}.json'.format(filename), 'w', encoding="utf-8") as json_file:  
		json.dump(data, json_file)
