import numpy as np

def purge_generation(interaction_maps, pop, safe_zones=[[0+5, 75+5, 0+5, 150+5]]):
	safe_pop = []
	for individual in pop:
		unsafe = True
		for zones in safe_zones:
			if individual["xt"]>=zones[0] and individual["xt"]<=zones[1] and individual["yt"]>=zones[2] and individual["yt"]<=zones[3]:
				unsafe=False
		if not unsafe:
			safe_pop.append(individual)
	return safe_pop