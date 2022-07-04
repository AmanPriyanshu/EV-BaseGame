import numpy as np
from individual import random_individual_generator, read_individual_states, take_individual_next_step
import cv2
import pandas as pd


class Environment:
	def __init__(self, random_individual_generator_func, read_individual_states_func, take_individual_next_step_func, height=300, width=300, safe_zones=[[150, 150, 0, 300]], population_size=100, total_generations=10, margin=5):
		self.margin = margin
		self.read_individual_states_func = read_individual_states_func
		self.random_individual_generator_func = random_individual_generator_func
		self.take_individual_next_step_func = take_individual_next_step_func
		self.height = height
		self.width = width
		self.safe_zones = safe_zones
		self.interaction_maps, self.colourful_maps = self.generate_map()
		self.population_size = population_size
		self.total_generations = total_generations
		self.representation_genome = {"00": "A", "01": "G", "10": "C", "11": "T"}
		self.current_t = 0

	def generate_map(self):
		interaction_maps = np.zeros((self.height+self.margin*2, self.width+self.margin*2))
		colourful_maps = np.zeros((self.height+self.margin*2, self.width+self.margin*2, 3))+255
		interaction_maps[0:self.margin, :] = 1
		interaction_maps[:, 0:self.margin] = 1
		interaction_maps[self.margin+self.height:self.height+2*self.margin, :] = 1
		interaction_maps[:, self.margin+self.height:self.height+2*self.margin] = 1
		colourful_maps[0:self.margin, :, :] = 0
		colourful_maps[:, 0:self.margin, :] = 0
		colourful_maps[self.margin+self.height:self.height+2*self.margin, :, :] = 0
		colourful_maps[:, self.margin+self.height:self.height+2*self.margin, :] = 0
		return interaction_maps, colourful_maps

	def generate_random_positions(self):
		y_array, x_array = [], []
		while len(y_array)!=self.population_size:
			y = np.random.randint(low=self.margin, high=self.height+self.margin)
			x = np.random.randint(low=self.margin, high=self.width+self.margin)
			not_present = True
			for i,j in zip(x_array, y_array):
				if i==x and j==y:
					not_present = False
			if not_present:
				y_array.append(y)
				x_array.append(x)
		return x_array, y_array

	def randomly_populate(self):
		pop = []
		x_array, y_array = self.generate_random_positions()
		for i in range(self.population_size):
			individual = {"bin_genes": self.random_individual_generator_func(),"yt": y_array[i], "xt": x_array[i], "prev_direction": "north", "moving": 0}
			pop.append(individual)
		return pop

	def draw_map(self, pop, t=0):
		self.generate_map()
		record = {"x": [], "y": [], "R": [], "G": [], "B": [], "prev_direction": [], "moving": []}
		record.update({"gene_grp_"+str(i+1):[] for i in range(len(pop[0]["bin_genes"]))})
		for individual in pop:
			record["x"].append(individual["xt"])
			record["y"].append(individual["yt"])
			record["prev_direction"].append(individual["prev_direction"])
			record["moving"].append(individual["moving"])
			r,g,b = 0.0,0.0,0.0
			rgb = []
			for idx, gene_group in enumerate(individual["bin_genes"]):
				record["gene_grp_"+str(idx+1)].append("".join([self.representation_genome[gene_group[i:i+2]] for i in range(0, len(gene_group), 2)]))
				rgb_gene_group = gene_group+"00"
				rgb_gene_group = [int(rgb_gene_group[i:i+8].encode(), 2) for i in range(0, len(rgb_gene_group), 8)]
				rgb.append(rgb_gene_group)
			rgb = [int(i) for i in np.mean(rgb, axis=0)]
			for i,j in enumerate("RGB"):
				record[j].append(rgb[i])
				self.colourful_maps[record["x"][-1]][record["y"][-1]][i] = record[j][-1]
				self.interaction_maps[record["x"][-1]][record["y"][-1]] = 2
		record = pd.DataFrame(record)
		record.to_csv("./env_pops/time_"+"0"*(len(str(self.total_generations)) - len(str(self.current_t)))+str(self.current_t)+".csv", index=False)
		resized_img = cv2.resize(self.colourful_maps, (self.width*2, self.height*2), interpolation = cv2.INTER_AREA)
		cv2.imwrite("./env_maps/time_"+"0"*(len(str(self.total_generations)) - len(str(self.current_t)))+str(self.current_t)+".png", resized_img)

	def take_next_steps(self, pop):
		for individual in pop:
			state = self.read_individual_states_func(individual, self.interaction_maps[individual["yt"]-2:individual["yt"]+3, individual["xt"]-2:individual["xt"]+3])
			self.take_individual_next_step_func(state, individual)

			exit()

if __name__ == '__main__':
	env = Environment(random_individual_generator, read_individual_states, take_individual_next_step, population_size=100)
	pop = env.randomly_populate()
	env.draw_map(pop)
	env.take_next_steps(pop)