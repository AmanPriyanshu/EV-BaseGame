import numpy as np

def random_individual_generator(num_chromosomes=5):
	genes = np.random.rand(num_chromosomes*22)
	genes = ''.join([i for i in np.where(genes>0.5, "1", "0")])
	genes = [genes[i:i+22] for i in range(0, len(genes), 22)]
	return genes

if __name__ == '__main__':
	random_individual_generator()