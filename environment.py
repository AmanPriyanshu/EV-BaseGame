import numpy as np

class Environment:
	def __init__(self, height=300, width=300, safe_zones=[[150, 150, 0, 300]], population_size=100):
		self.height = height
		self.width = width
		self.safe_zones = safe_zones
		self.interaction_maps, self.colourful_maps = self.generate_map()
		self.population_size = population_size

	def generate_map(self):
		interaction_maps = np.zeros((self.height, self.width))
		colourful_maps = np.zeros((self.height, self.width, 3))
		return interaction_maps, colourful_maps

	def randomly_populate(self, random_individual_generator_func):
		pass

