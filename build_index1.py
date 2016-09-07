from Subtitle import Subtitle
from tokenizer import Tokenizer
import pickle
import pandas as pd
import os
import config as CONFIG

with open(CONFIG.datasets_path + "filtered_index.p", 'rb') as f:
  subtitles_index = pickle.load(f, encoding='latin-1')

# THIS NEEDS TO BE STOPPED AND RESTARTED. SAVE LAST MOVIE, READ EXISTING FILE, LOAD INTO MEMORY AND CONTINUE

subs = subtitles_index["IDSubtitleFile"]
tokenizer = Tokenizer()
index = {}
for s in subs:
  print(s)
  sub = Subtitle(int(s))
  tokens = tokenizer.full_run(sub.full_text())

  for token in tokens:
    if token in index:
      index[token].append(s)
    else:
      index[token] = [s]

with open(CONFIG.datasets_path + "manual_inverted_index.p", 'wb') as file:
  pickle.dump(index, file, protocol=pickle.HIGHEST_PROTOCOL)
