import pandas as pd
import config as CONFIG
import pickle
from Subtitle import Subtitle
from tokenizer import Tokenizer

with open(CONFIG.datasets_path + "filtered_index.p", 'rb') as f:
  sub_data = pickle.load(f)

tokenizer = Tokenizer()
data = sub_data[['IDSubtitleFile','MovieYear']]

result = {}
for row in data.itertuples():
  if row.MovieYear == 0:
    continue
  sub = Subtitle(int(row.IDSubtitleFile))
  tokens = tokenizer.full_run(sub.full_text())
  if row.MovieYear in result:
    result[row.MovieYear] += len(tokens)
  else:
    result[row.MovieYear] = len(tokens)

try:
  with open(CONFIG.datasets_path + "word_count.p", 'wb') as file:
    pickle.dump(result, file, protocol=pickle.HIGHEST_PROTOCOL)
except:
  print(count)
