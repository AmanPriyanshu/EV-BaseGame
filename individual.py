import numpy as np

def random_individual_generator(num_chromosomes=5):
	genes = np.random.rand(num_chromosomes*22)
	genes = ''.join([i for i in np.where(genes>0.5, "1", "0")])
	genes = [genes[i:i+22] for i in range(0, len(genes), 22)]
	return genes

def read_individual_states(individual, surroundings, directions=["north", "south", "west", "east"]):
	state = {"prev_direction": individual["prev_direction"], "moving": individual["moving"], "x": individual["xt"], "y": individual["yt"]}
	numeric_state = [directions.index(state["prev_direction"]), state["moving"], state["x"], state["y"]]
	for i in range(5):
		for j in range(5):
			if i==2 and j==2:
				continue
			state.update({"surround_space_pixel_"+str(i)+str(j):surroundings[i][j]})
			numeric_state.append(surroundings[i][j])
	return state, numeric_state

def take_individual_next_step(state, individual, directions=["north", "south", "west", "east"]):
	output_impulses = {i:0.0 for i in range(5)}
	for gene_grp in individual["bin_genes"]:
		fires = int(gene_grp[0])
		if fires:
			input_param = int(gene_grp[1:6].encode(), 2)%28
			output_neuron = int(gene_grp[6:9].encode(), 2)%5
			val = (int(gene_grp[9:].encode(), 2)-4096)/1000
			output_impulses[output_neuron] += state[input_param]*val
	output_impulses = np.array([output_impulses[i] for i in range(5)])
	output_impulses = np.exp(output_impulses)
	output_impulses = output_impulses/np.sum(output_impulses)
	chosen_outcome = np.argmax(output_impulses)
	x = individual["xt"]
	y = individual["yt"]
	if chosen_outcome==0:
		moving = 0
		direction = individual["prev_direction"]
	else:
		moving = 1
		if chosen_outcome==1:
			direction = individual["prev_direction"]
			if individual["prev_direction"]=="north":
				y += -1
			elif individual["prev_direction"]=="south":
				y += 1
			elif individual["prev_direction"]=="east":
				x += 1
			elif individual["prev_direction"]=="west":
				x += -1
		elif chosen_outcome==2:
			if individual["prev_direction"]=="north":
				direction = "west"
			elif individual["prev_direction"]=="south":
				direction = "east"
			elif individual["prev_direction"]=="east":
				direction = "north"
			elif individual["prev_direction"]=="west":
				direction = "south"
		elif chosen_outcome==3:
			if individual["prev_direction"]=="north":
				direction = "east"
			elif individual["prev_direction"]=="south":
				direction = "west"
			elif individual["prev_direction"]=="east":
				direction = "south"
			elif individual["prev_direction"]=="west":
				direction = "north"
		elif chosen_outcome==4:
			if individual["prev_direction"]=="north":
				direction = "south"
			elif individual["prev_direction"]=="south":
				direction = "north"
			elif individual["prev_direction"]=="east":
				direction = "west"
			elif individual["prev_direction"]=="west":
				direction = "east"
	new_state = {"bin_genes": individual["bin_genes"], "yt": y, "xt": x, "prev_direction": direction, "moving": moving}
	return output_impulses, new_state

if __name__ == '__main__':
	random_individual_generator()