import networkx as nx
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def visualize_genome_sequence(sequences, representation, input_params, output_neurons, path="mind.png"):
	plt.cla()
	plt.clf()
	G = nx.Graph()
	for sequence in sequences:
		bin_sequence = "".join([representation[i] for i in sequence])
		active = int(bin_sequence[0])
		input_param = int(bin_sequence[1:6].encode(), 2)%28
		output_neuron = int(bin_sequence[6:9].encode(), 2)%5
		val = (int(bin_sequence[9:].encode(), 2)-4096)/1000
		if active:
			G.add_nodes_from([(input_params[input_param], {"color": "olive"}), (output_neurons[output_neuron], {"color": "green" if output_neuron!=0 else "red"})])
			G.add_edge(input_params[input_param], output_neurons[output_neuron], weight=abs(val), color='blue' if val>0 else 'purple')
	input_neuron_indices, output_neuron_indices = [], []
	for idx, node in enumerate(G.nodes):
		if G.nodes[node]['color'] == 'olive':
			input_neuron_indices.append(idx)
		else:
			output_neuron_indices.append(idx)
	positions = {}
	for idx, node in enumerate(G.nodes):
		if idx in input_neuron_indices:
			positions.update({node: (input_neuron_indices.index(idx)*2, 2)})
		else:
			positions.update({node: (output_neuron_indices.index(idx)*2, 0)})
	nx.draw(G, pos=positions, node_color=[G.nodes[node]['color'] for node in G.nodes], edge_color=[G.edges[edge]['color'] for edge in G.edges], width=[G.edges[edge]['weight'] for edge in G.edges], with_labels=True)
	plt.draw()
	plt.savefig(path)



if __name__ == '__main__':
	representation={"A": "00", "G": "01", "C": "10", "T": "11"}
	input_params = ["prev_direction", "moving", "x", "y"]
	for i in range(5):
		for j in range(5):
			if i==2 and j==2:
				continue
			input_params.append("surround_space_pixel_"+str(i)+str(j))
	output_neurons = ["stay_at_rest"] + ["move_"+i for i in ["north", "south", "east", "west"]]
	sequences = ["TTCCGGCACTG", "TTAAGGATAAG"]
	visualize_genome_sequence(sequences, representation, input_params, output_neurons)