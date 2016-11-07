from subtitle import Subtitle
from tokenizer import Tokenizer
import pickle
import pandas as pd
import os
import config as CONFIG

with open(CONFIG.datasets_path + "filtered_index.p", 'rb') as f:
  subtitles_index = pickle.load(f, encoding='latin-1')

tokenizer = Tokenizer()
full_index_path = CONFIG.datasets_path + "full_per_year"
if os.path.exists(full_index_path):
  files = os.listdir(full_index_path)
  start = 1930 + len(files)
else:
  os.makedirs(full_index_path)
  start = 1930

print("STARTS IN: ", start)
for year in range(start,2016):
  print("START YEAR: ", year)
  subs = subtitles_index[subtitles_index.MovieYear == year][["IDSubtitleFile", "MovieYear"]]
  index = {}
  for row in subs.itertuples():
    subId = row.IDSubtitleFile
    print(subId)
    sub = Subtitle(int(subId))

    for line in sub.raw_sub:
      tokens = tokenizer.full_run(line.text)
      timestamp = line.start.__str__()
      for token in tokens:
        if not token in index:
          index[token] = {}
        if not subId in index[token]:
          index[token][subId] = []
        index[token][subId].append(timestamp)


  with open(full_index_path + "/index_" + str(year) + ".p", 'wb') as file:
    pickle.dump(index, file, protocol=pickle.HIGHEST_PROTOCOL)
