import numpy as np
from individual import random_individual_generator, read_individual_states, take_individual_next_step, make_children_function
from purger import purge_generation
import cv2
import pandas as pd
import warnings
import os
from tqdm import trange

warnings.filterwarnings('ignore')


class Environment:
	def __init__(self, random_individual_generator_func, read_individual_states_func, take_individual_next_step_func, purge_generation_func, make_children_func, height=300, width=300, population_size=100, total_generations=10, margin=5, iterations_per_generation=30):
		self.iterations_per_generation = iterations_per_generation
		self.make_children_func = make_children_func
		self.purge_generation_func = purge_generation_func
		self.margin = margin
		self.read_individual_states_func = read_individual_states_func
		self.random_individual_generator_func = random_individual_generator_func
		self.take_individual_next_step_func = take_individual_next_step_func
		self.height = height
		self.width = width
		self.interaction_maps, self.colourful_maps = self.generate_map()
		self.population_size = population_size
		self.total_generations = total_generations
		self.representation_genome = {"00": "A", "01": "G", "10": "C", "11": "T"}
		self.current_t = 0
		self.gen_counter = 0

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

	def draw_map(self, pop, t=0, path_survived=False):
		self.interaction_maps, self.colourful_maps = self.generate_map()
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
				self.colourful_maps[record["y"][-1]][record["x"][-1]][i] = record[j][-1]
				self.interaction_maps[record["y"][-1]][record["x"][-1]] = 2
		record = pd.DataFrame(record)
		if not path_survived:
			if not os.path.exists("./env_pops/gen_"+"0"*(len(str(self.total_generations)) - len(str(self.gen_counter)))+str(self.gen_counter)+"/"):
				os.mkdir("./env_pops/gen_"+"0"*(len(str(self.total_generations)) - len(str(self.gen_counter)))+str(self.gen_counter)+"/")
				os.mkdir("./env_maps/gen_"+"0"*(len(str(self.total_generations)) - len(str(self.gen_counter)))+str(self.gen_counter)+"/")
			record.to_csv("./env_pops/gen_"+"0"*(len(str(self.total_generations)) - len(str(self.gen_counter)))+str(self.gen_counter)+"/time_"+"0"*(len(str(self.iterations_per_generation)) - len(str(self.current_t)))+str(self.current_t)+".csv", index=False)
			resized_img = cv2.resize(self.colourful_maps, (self.width*2, self.height*2), interpolation = cv2.INTER_AREA)
			cv2.imwrite("./env_maps/gen_"+"0"*(len(str(self.total_generations)) - len(str(self.gen_counter)))+str(self.gen_counter)+"/time_"+"0"*(len(str(self.iterations_per_generation)) - len(str(self.current_t)))+str(self.current_t)+".png", resized_img)
		else:
			record.to_csv("./env_pops/gen_"+"0"*(len(str(self.total_generations)) - len(str(self.gen_counter)))+str(self.gen_counter)+"_survived.csv", index=False)
			resized_img = cv2.resize(self.colourful_maps, (self.width*2, self.height*2), interpolation = cv2.INTER_AREA)
			cv2.imwrite("./env_maps/gen_"+"0"*(len(str(self.total_generations)) - len(str(self.gen_counter)))+str(self.gen_counter)+"_survived.png", resized_img)

	def take_next_steps(self, pop):
		new_pop = []
		x_array, y_array = [individual["xt"] for individual in pop], [individual["yt"] for individual in pop]
		for idx, individual in enumerate(pop):
			state, numeric_state = self.read_individual_states_func(individual, self.interaction_maps[individual["yt"]-2:individual["yt"]+3, individual["xt"]-2:individual["xt"]+3])
			output_impulses, new_state = self.take_individual_next_step_func(numeric_state, individual)
			if new_state["xt"]<self.margin:
				new_state["xt"] += 1
			if new_state["xt"]>self.margin+self.width-1:
				new_state["xt"] -= 1
			if new_state["yt"]<self.margin:
				new_state["yt"] += 1
			if new_state["yt"]>self.margin+self.width-1:
				new_state["yt"] -= 1
			not_present = True
			for idx_j, (i,j) in enumerate(zip(x_array, y_array)):
				if idx_j==idx:
					continue
				if i==new_state["xt"] and j==new_state["yt"]:
					not_present = False
			if not_present:
				x_array.append(new_state["xt"])
				y_array.append(new_state["yt"])
			else:
				new_state["xt"] = individual["xt"]
				new_state["yt"] = individual["yt"]
			new_pop.append(new_state)
		self.current_t += 1
		return new_pop

	def run_generational_iters(self, pop):
		for iter_num in trange(self.iterations_per_generation, desc="generation_"+str(self.gen_counter)):
			env.draw_map(pop)
			pop = env.take_next_steps(pop)
		env.draw_map(pop)
		return pop

	def purge(self, pop):
		alive_pop = self.purge_generation_func(self.interaction_maps, pop)
		env.draw_map(alive_pop, path_survived=True)
		return alive_pop

	def make_children(self, pop):
		children_required = self.population_size - len(pop)
		child_genes = []
		for idx in range(children_required):
			i,j = np.random.randint(len(pop), size=2)
			child = self.make_children_func(pop[i],pop[j])
			child_genes.append(child)
		parent_genes = [individual["bin_genes"] for individual in pop]
		return child_genes+parent_genes

	def distribute_new_gene_population(self, gene_pool):
		self.gen_counter+=1
		self.current_t = 0
		pop = []
		x_array, y_array = self.generate_random_positions()
		for i in range(self.population_size):
			individual = {"bin_genes": gene_pool[i],"yt": y_array[i], "xt": x_array[i], "prev_direction": "north", "moving": 0}
			pop.append(individual)
		return pop

	def run_experiment(self):
		pop = env.randomly_populate()
		for gen_no in range(self.total_generations):
			pop = self.run_generational_iters(pop)
			pop = self.purge(pop)
			print(len(pop), "survived!")
			gene_pool = self.make_children(pop)
			pop = self.distribute_new_gene_population(gene_pool)
		self.draw_map(pop)

if __name__ == '__main__':
	env = Environment(random_individual_generator, read_individual_states, take_individual_next_step, purge_generation, make_children_function, population_size=1000, iterations_per_generation=150)
	env.run_experiment()