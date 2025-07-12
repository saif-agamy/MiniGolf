import pygame 
import json


class Tile_Map:
	def __init__(self, game):
		self.game = game
		self.tile_size = 32
		self.tile_map = {} # This Will BE {'2;3': {'type': 'ground', 'pos': (2, 3)}} --> This Is Just One Tile Which Has The Position (2, 3)

	def render(self, window):
		for pos in self.tile_map:
			tile = self.tile_map[pos] 
			window.blit(self.game.assets[tile['type']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

	def save(self, file_name):
		f = open(file_name, 'w')
		json.dump({'tile_map': self.tile_map, 'tile_size': self.tile_size}, f)
		f.close()

	def load(self, file_name):
		f = open(file_name, 'r')
		map_data = json.load(f)
		f.close()

		self.tile_map = map_data['tile_map']
		self.tile_size = map_data['tile_size']

	def change_hole_pos(self, new_pos):
		for pos in self.tile_map:
			tile = self.tile_map[pos]
			if tile['type'] == 'hole':
				tile['pos'] = new_pos