# July 12, 2021, images downloader
import os

print(f'Current Directory = {os.getcwd()}')

import EDA_Yoga as EDA_Yoga

path = 'data/yoga_dataset_links'

files = os.listdir(path)
files.sort()
files.remove('.DS_Store')

num_files = len(files)
counter = 1
for file in files:
    print(f'Processing file {counter} of {num_files}, {file}')
    EDA_Yoga.File_of_82(path + '/' + file, 
           path_2_dump='img/', 
           img_display=False)
    counter += 1