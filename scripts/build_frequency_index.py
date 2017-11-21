import sys
sys.path.append('..')
from repo.subtitle import Subtitle
from repo.tokenizer import Tokenizer
from repo import config as CONFIG
import pickle
import pandas as pd
import os

with open(CONFIG.datasets_path + "filtered_index_2017.p", 'rb') as f:
  subtitles_index = pickle.load(f, encoding='latin-1')

subs = subtitles_index[subtitles_index.MovieYear >= 1930][["IDSubtitleFile", "MovieYear"]]
tokenizer = Tokenizer()
index = {}
for row in subs.itertuples():
  print(row.IDSubtitleFile)
  try:
    sub = Subtitle(int(row.IDSubtitleFile))
    year = int(row.MovieYear)
    tokens = tokenizer.full_run(sub.full_text())

    for token in tokens:
      if not token in index:
        index[token] = {}
      if not year in index[token]:
        index[token][year] = 0
      index[token][year] += 1
  except:
    print("ERROR")


with open(CONFIG.datasets_path + "frequency_index_2017.p", 'wb') as file:
  pickle.dump(index, file, protocol=pickle.HIGHEST_PROTOCOL)
