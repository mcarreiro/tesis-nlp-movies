import sys
sys.path.append('..')
from repo import config as CONFIG
import pandas as pd
import pickle

with open(CONFIG.datasets_path + "filtered_index.p", 'rb') as f:
  sub_data = pickle.load(f)

gr = sub_data[['MovieID','MovieYear']].groupby('MovieYear')
count = gr.count().to_dict()['MovieID']

with open(CONFIG.datasets_path + "movie_count.p", 'wb') as file:
  pickle.dump(count, file, protocol=pickle.HIGHEST_PROTOCOL)
