from subtitle import Subtitle
from tokenizer import Tokenizer
import pickle
import pandas as pd
import os
import config as CONFIG

with open(CONFIG.datasets_path + "full_per_year/index_all.p", 'rb') as f:
  full_index = pickle.load(f)

new_full_index = {}
for word,years in full_index.items():
  mentions = 0
  movie_count = 0
  new_full_index[word] = {}
  for year,movies in years.items():
    new_full_index[word][year] = {}
    for subId,times in movies.items():
      new_full_index[word][year][str(int(subId))] = times
      mentions += len(times)
      movie_count += 1
  if mentions <= 80 or movie_count < 10:
    del new_full_index[word]


with open(CONFIG.datasets_path + "full_times_index.p", 'wb') as file:
  pickle.dump(new_full_index, file, protocol=pickle.HIGHEST_PROTOCOL)
