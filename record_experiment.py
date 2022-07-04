import os
from PIL import Image
from tqdm import tqdm

def main(base_path="./env_maps/"):
	directories = sorted([base_path+i+'/' for i in os.listdir(base_path) if '.' not in i])
	selected_directories = [v for i,v in enumerate(directories) if (i+1)%5==0 or i==0]
	for directory in tqdm(selected_directories, desc="converting2gifs"):
		output_file = directory.replace('./env_maps/', './env_gifs/')[:-1]+'.gif'
		images = [Image.open(file) for file in sorted([directory+i for i in os.listdir(directory)])]
		images[0].save(output_file, append_images=images[1:], duration=1/75, save_all=True, loop=0, optimize=False)

if __name__ == '__main__':
	main()