from subtitle import Subtitle
from tokenizer import Tokenizer
import pickle
import pandas as pd
import os
import config as CONFIG

full_index_path = CONFIG.datasets_path + "full_per_year"
files = os.listdir(full_index_path)

index = {}
for year in range(1930,2016):
  file_name = full_index_path + "/index_" + str(year) + ".p"
  with open(file_name, 'rb') as f:
    partial = pickle.load(f, encoding='latin-1')
  for word, occurrences in partial.items():
    if not word in index:
      index[word] = {}
    index[word][year] = occurrences

with open(full_index_path + "/index_all.p", 'wb') as file:
  pickle.dump(index, file, protocol=pickle.HIGHEST_PROTOCOL)
