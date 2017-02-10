from subtitle import Subtitle
from tokenizer import Tokenizer
import pickle
import pandas as pd
import os
import config as CONFIG

full_index_path = CONFIG.datasets_path + "full_per_year_2017"
files = os.listdir(full_index_path)

index = {}
for year in range(1930,2016):
  file_name = full_index_path + "/index_" + str(year) + ".p"
  with open(file_name, 'rb') as f:
    partial = pickle.load(f, encoding='latin-1')
  for word, occurrences in partial.items():
    movie_count = 0
    if not word in index:
      index[word] = {}
    index[word][year] = occurrences
    movie_count += len(occurrences)
  if movie_count < 10:
    del index[word]

with open(full_index_path + "/index_all_2017.p", 'wb') as file:
  pickle.dump(index, file, protocol=pickle.HIGHEST_PROTOCOL)
