import networkx as nx
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
from tqdm import tqdm

def visualize_genome_sequence(sequences, representation, input_params, output_neurons, path="mind.png", gap=4):
	plt.cla()
	plt.clf()
	G = nx.Graph()
	for sequence in sequences:
		bin_sequence = sequence#"".join([representation[i] for i in sequence])
		active = int(bin_sequence[0])
		input_param = int(bin_sequence[1:6].encode(), 2)%28
		output_neuron = int(bin_sequence[6:9].encode(), 2)%5
		val = (int(bin_sequence[9:].encode(), 2)-4096)/1000
		if active:
			G.add_nodes_from([(input_params[input_param], {"color": "olive"}), (output_neurons[output_neuron], {"color": "green" if output_neuron!=0 else "red"})])
			G.add_edge(input_params[input_param], output_neurons[output_neuron], weight=abs(val)**1.5, color='blue' if val>0 else 'purple')
	input_neuron_indices, output_neuron_indices = [], []
	for idx, node in enumerate(G.nodes):
		if G.nodes[node]['color'] == 'olive':
			input_neuron_indices.append(idx)
		else:
			output_neuron_indices.append(idx)
	positions = {}
	for idx, node in enumerate(G.nodes):
		if idx in input_neuron_indices:
			positions.update({node: (0, input_neuron_indices.index(idx)*gap)})
		else:
			positions.update({node: (2, output_neuron_indices.index(idx)*gap)})
	nx.draw(G, pos=positions, node_color=[G.nodes[node]['color'] for node in G.nodes], edge_color=[G.edges[edge]['color'] for edge in G.edges], width=[G.edges[edge]['weight'] for edge in G.edges], with_labels=True)
	plt.draw()
	plt.savefig(path, bbox_inches="tight")

def generate_centroid_genes(representation, path="./env_pops/gen_100/time_000.csv"):
	df = pd.read_csv(path)
	df = df.values
	df = df.T[7:].T
	sequences = []
	for col in df.T:
		bin_values = []
		for val in col:
			bin_sequence = "".join([representation[i] for i in val])
			bin_values.append(bin_sequence)
		main_descs, main_counts = np.unique([i[:9] for i in bin_values], return_counts=True)
		main_inp_out_unit = main_descs[np.argmax(main_counts)]
		active_values = int(np.mean([(int(i[9:].encode(), 2)-4096)/1000 for i in bin_values if i[:9]==main_inp_out_unit])*1000+4096)
		active_value = np.binary_repr(active_values, width=13)
		sequence = main_inp_out_unit+active_value
		sequences.append(sequence)
	return sequences

def generate_all_minds(path="./env_pops/"):
	representation={"A": "00", "G": "01", "C": "10", "T": "11"}
	input_params = ["prev_direction", "moving", "x", "y"]
	for i in range(5):
		for j in range(5):
			if i==2 and j==2:
				continue
			input_params.append("surround_space\n_pixel_"+str(i)+str(j))
	output_neurons = ["stay_at_rest"] + ["move_"+i for i in ["north", "south", "east", "west"]]
	for directory in tqdm(sorted([path+i for i in os.listdir(path) if '.' in i]), desc="generating_mind_graphs"):
		path = directory
		sequences = generate_centroid_genes(representation, path=path)
		output_path = directory.replace('env_pops', 'env_mind').replace('.csv','.png')
		visualize_genome_sequence(sequences, representation, input_params, output_neurons, path=output_path)

if __name__ == '__main__':
	generate_all_minds()