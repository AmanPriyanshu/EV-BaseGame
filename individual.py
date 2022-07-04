import numpy as np

def random_individual_generator(num_chromosomes=5):
	genes = np.random.rand(num_chromosomes*22)
	genes = ''.join([i for i in np.where(genes>0.5, "1", "0")])
	genes = [genes[i:i+22] for i in range(0, len(genes), 22)]
	return genes

def read_individual_states(individual, surroundings):
	state = {"prev_direction": individual["prev_direction"], "moving": individual["moving"], "x": individual["xt"], "y": individual["yt"]}
	for i in range(5):
		for j in range(5):
			if i==2 and j==2:
				continue
			state.update({"surround_space_pixel_"+str(i)+str(j):surroundings[i][j]}) 
	return state

def take_individual_next_step(state, individual):
	for gene_grp in individual["bin_genes"]:
		fires = int(gene_grp[0])
		if fires:
			input_param = int(gene_grp[1:6].encode(), 2)%28
			print(input_param)

if __name__ == '__main__':
	random_individual_generator()