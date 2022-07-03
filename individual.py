import numpy as np

def random_individual_generator(num_chromosomes=5):
	genes = np.random.rand(size=22)
	print(genes)

if __name__ == '__main__':
	random_individual_generator()