from globals import *

import alife

import random
import os

def prettify_string_array(array, max_length):
	"""Returns a human readable string from an array of strings."""
	_string = ''
	
	_i = 0
	for entry in array:
		if len(_string) > max_length:
			_string += ', and %s more.' % (_i+1)
			
			break
		
		if _i == 0:
			_string += entry
		elif 0<_i<len(array)-1:
			_string += ', %s' % entry
		elif _i == len(array)-1:
			_string += ' and %s.' % entry
		
		_i += 1
	
	return _string

def get_name(life):
	if random.randint(0, 1):
		return ' '.join(life['name'])
	else:
		return 'He'

def _load_strings(a, directory, filenames):
	for filename in [f for f in filenames if f.count('.txt')]:
		_map_name = filename.strip('.txt')
		TEXT_MAP[_map_name] = []
		
		with open(os.path.join(directory, filename), 'r') as e:
			TEXT_MAP[_map_name].extend([line.strip() for line in e.readlines()])

def load_strings():
	try:
		os.path.walk(TEXT_DIR, _load_strings, None)
	except:
		raise Exception('Error loading strings.')

def generate_place_name():
	if not TEXT_MAP['places']:
		return 'Zoolandia'
	
	return TEXT_MAP['places'].pop(random.randint(0, len(TEXT_MAP['places'])-1))

def generate_first_and_last_name_from_species(species):
	_map_first_names = '%s_first_names' % species
	_map_last_names = '%s_last_names' % species
	
	if not TEXT_MAP[_map_first_names] or not TEXT_MAP[_map_last_names]:
		return ('Wayne', 'Brady')
	
	_first_name = TEXT_MAP[_map_first_names].pop(random.randint(0, len(TEXT_MAP[_map_first_names])-1))
	_last_name = TEXT_MAP[_map_last_names].pop(random.randint(0, len(TEXT_MAP[_map_last_names])-1))
	
	return (_first_name, _last_name)

def format_injury(injury):
	if injury['lodged_item']:
		return 'a %s lodged in the %s' % (injury['lodged_item']['name'], injury['limb'])
	elif injury['artery_ruptured']:
		return 'a ruptured artery in the %s' % injury['limb']
	elif injury['cut']:
		return 'a cut to the %s' % injury['limb']
	
	return 'nothing in particular.'

def generate_memory_phrase(memory):
	_details = [key for key in memory.keys() if not key == 'text']
	_memory_age = WORLD_INFO['ticks']-memory['time_created']
	_topic = memory['text']
	
	if _topic == 'friendly':
		return '%s seems like a good guy.' % (' '.join(LIFE[memory['target']]['name']))
	else:
		print 'DIDNT HAVE A PHRASE FOR',_topic

def get_description(life):
	_facts = []
	
	_group_threshold = alife.stats.get_max_group_size(life)
	if _group_threshold >= alife.stats.MAX_SOCIABILITY*.9:
		_facts.append('{pn} {prefers} large groups.')
	elif _group_threshold <= alife.stats.MAX_SOCIABILITY*.4:
		_facts.append('{pn} {avoids} groups.')