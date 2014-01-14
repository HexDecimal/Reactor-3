from globals import *

import graphics as gfx
import life as lfe

import language
import numbers
import effects
import spawns
import alife
import items

import random

def create_heli_crash(kind):
	while 1:
		chunk_key = random.choice(WORLD_INFO['chunk_map'])
		
		_walkable = alife.chunks.get_walkable_areas(chunk_key)
		if not _walkable:
			continue
		
def drop_cache(item_names):
	while 1:
		_chunk_key = random.choice(WORLD_INFO['chunk_map'].keys())
		_chunk = alife.chunks.get_chunk(_chunk_key)
		
		if _chunk['type'] == 'other':
			break
	
	for item in item_names:
		_pos = random.choice(_chunk['ground'])
		_item = ITEMS[items.create_item(item, position=[_pos[0], _pos[1], 2])]
		
		for life in LIFE.values():
			lfe.memory(life, 'cache_drop', chunk_key=_chunk_key)
			#alife.survival.add_needed_item(life,
			#                               {'pos': _item['pos'][:]},
			#                               satisfy_if=alife.action.make_small_script(function='always'),
			#                               satisfy_callback=alife.action.make_small_script(function='consume'))
			#alife.brain.remember_item(life, _item)
	
	gfx.message('You see something parachuting to the ground.')
	print _chunk['pos']

def get_player_situation():
	if not SETTINGS['controlling']:
		return False
	
	_life = LIFE[SETTINGS['controlling']]
	
	_situation = {}
	_situation['armed'] = alife.combat.has_potentially_usable_weapon(_life)
	_situation['friends'] = len([l for l in _life['know'].values() if l['alignment'] in ['trust', 'feign_trust']])
	
	return _situation

def get_group_leader_with_motive(group_motive, online=False):
	for life in LIFE.values():
		if not (life['online'] or not online) or not life['group'] or not alife.groups.is_leader(life, life['group'], life['id']) or SETTINGS['controlling'] == life['id']:
			continue
		
		if alife.groups.get_motive(life, life['group']) == group_motive:
			return life['id']
	
	return None

def spawn_life(life_type, position, event_time, **kwargs):
	_life = {'type': life_type, 'position': position[:]}
	_life.update(**kwargs)
	         
	WORLD_INFO['scheme'].append({'life': _life, 'time': event_time})

def order_group(life, group_id, stage, event_time, **kwargs):
	WORLD_INFO['scheme'].append({'group': group_id, 'member': life['id'], 'stage': stage, 'flags': kwargs, 'time': WORLD_INFO['ticks']+event_time})

def broadcast(messages, event_time):
	_time = WORLD_INFO['ticks']+event_time
	
	for entry in messages:
		if 'source' in entry:
			_source = entry['source']
		else:
			_source = '???'		
		
		WORLD_INFO['scheme'].append({'radio': [_source, entry['text']], 'time': _time})
		
		_time += int(round(len(entry['text'])*1.25))

def form_scheme():
	if WORLD_INFO['scheme']:
		return False
	
	_player_situation = get_player_situation()
	
	#if _player_situation['armed']:
	_i = random.randint(0, 3)+10
	
	if _i == 1:
		_military_group_leader = get_group_leader_with_motive('military')
		_bandit_group_leader = get_group_leader_with_motive('crime', online=False)
		
		#TODO: Actual bandit camp location
		if _military_group_leader and _bandit_group_leader:
			_bandit_group_location = lfe.get_current_chunk_id(LIFE[_bandit_group_leader])
			order_group(LIFE[_military_group_leader], LIFE[_military_group_leader]['group'], STAGE_RAIDING, 30, chunk_key=_bandit_group_location)
			alife.groups.discover_group(LIFE[_military_group_leader], LIFE[_bandit_group_leader]['group'])
			alife.groups.declare_group_hostile(LIFE[_military_group_leader], LIFE[_military_group_leader]['group'], LIFE[_bandit_group_leader]['group'])
	
	elif _i == 2:
		_spawn_pos = spawns.get_spawn_in_ref('farms')
		_real_direction = language.get_real_direction(numbers.direction_to((MAP_SIZE[0]/2, MAP_SIZE[1]/2), _spawn_pos))
		
		spawn_life('loner', _spawn_pos, 35, injuries={'llowerleg': {'cut': 1}})

		_messages = [{'text': 'Hello? Can anyone hear me?'},
	                 {'text': 'Bandits robbed me and left me to bleed out...'},
	                 {'text': 'I\'m by a farm to the %s.' % _real_direction},
	                 {'text': 'They might still be around. Please hurry!'}]
		broadcast(_messages, 40)
	
	elif 1 == 1:
		_bandit_group_leader = get_group_leader_with_motive('crime')
		_military_group_leader = get_group_leader_with_motive('military', online=False)
		
		if _military_group_leader and _bandit_group_leader:
			_bandit_group_location = lfe.get_current_chunk_id(LIFE[_bandit_group_leader])
			_military_group_location = lfe.get_current_chunk_id(LIFE[_military_group_leader])
			order_group(LIFE[_bandit_group_leader], LIFE[_bandit_group_leader]['group'], STAGE_RAIDING, 300, chunk_key=_military_group_location)
			alife.groups.discover_group(LIFE[_bandit_group_leader], LIFE[_military_group_leader]['group'])
			alife.groups.declare_group_hostile(LIFE[_bandit_group_leader], LIFE[_bandit_group_leader]['group'], LIFE[_military_group_leader]['group'])

			_real_direction = language.get_real_direction(numbers.direction_to((MAP_SIZE[0]/2, MAP_SIZE[1]/2), alife.chunks.get_chunk(_military_group_location)['pos']))
		
			_messages = [{'text': 'Attention all neutral and bandit squads.'},
				         {'text': 'We finally got solid contact on military in the %s compound.' % _real_direction},
				         {'text': 'We\'re located near coords %s and heading out soon.' % (', '.join(_bandit_group_location.split(',')))}]
			broadcast(_messages, 40)
		
	#if not WORLD_INFO['scheme'] and WORLD_INFO['ticks'] < 100:
		#if 1==1:#random.randint(0, 5):
			
		#else: #TODO: Get group
		#	_bandit_raid_direction = 'north'
		#	
		#	_messages = [{'text': 'This is %s of %s, broadcasting to all.', 'source': 'Group Leader'},
		#                 {'text': 'We\'re in dire need of help near <location>.', 'source': 'Group Leader'},
		#                 {'text': 'A group of bandits is approaching from the %s.' % _bandit_raid_direction, 'source': 'Group Leader'},
		#                 {'text': 'If you are able to fight, please! We need fighters!', 'source': 'Group Leader'}]
		#	broadcast(_messages, 40)

def execute_scheme():
	if not WORLD_INFO['scheme']:
		return False
	
	_event = None
	
	for event in WORLD_INFO['scheme']:
		if event['time'] <= WORLD_INFO['ticks']:
			_event = event
			break
	
	if not _event:
		return False
	
	if 'radio' in _event:
		gfx.message('%s: %s' % (_event['radio'][0], _event['radio'][1]), style='radio')
	
	if 'life' in _event:
		_life = spawns.generate_life(_event['life']['type'], position=_event['life']['position'])[0]
		
		if 'injuries' in _event['life']:
			for limb in _event['life']['injuries']:
				lfe.add_wound(_life, limb, **_event['life']['injuries'][limb])
	
	if 'group' in _event:
		if 'stage' in _event:
			alife.groups.set_stage(LIFE[_event['member']], _event['group'], _event['stage'])
			
			if _event['stage'] == STAGE_RAIDING:
				alife.groups.raid(LIFE[_event['member']], _event['group'], _event['flags']['chunk_key'])
	
	WORLD_INFO['scheme'].pop(0)
