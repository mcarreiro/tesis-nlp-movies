from subtitle import Subtitle
from tokenizer import Tokenizer
import pickle
import pandas as pd
import os
import config as CONFIG
# import hunspell
from textblob import TextBlob
from textblob import Word
import operator

with open(CONFIG.datasets_path + "filtered_index_2017.p", 'rb') as f:
  subtitles_index = pickle.load(f, encoding='latin-1')

tokenizer = Tokenizer()
# Hunspell
# spellchecker = hunspell.HunSpell('/Users/vale/anaconda3/envs/tesis/hunspell_dictionaries/en_US.dic',
#                                  '/Users/vale/anaconda3/envs/tesis/hunspell_dictionaries/en_US.aff')

folder_path = CONFIG.datasets_path + "worst_spelled/"
if os.path.exists(folder_path):
  files = os.listdir(folder_path)
  start = 1930 + len(files)
else:
  os.makedirs(folder_path)
  start = 1930

print("STARTS IN: ", start)
for year in range(start,2016):
  print("HERE STARTS YEAR: ", year)
  subs = subtitles_index[subtitles_index.MovieYear == year][["IDSubtitleFile", "MovieYear"]]
  words = {}
  for row in subs.itertuples():
    subId = str(int(row.IDSubtitleFile))
    print(subId)
    try:
      sub = Subtitle(int(subId))
      tokens = tokenizer.full_run(sub.full_text())

      # Hunspell version
      # for token in tokens:
      #   ok = spellchecker.spell(w)   # check spelling
      #   if not ok:
      #       print("Palabra: ", w)
      #       suggestions = spellchecker.suggest(w)
      #       if len(suggestions) > 0:  # there are suggestions
      #           best = suggestions[0]
      #           print("Sug 1: ", best)
      #           if suggestions.length > 1:
      #             print("Sug 2: ", suggestions[1])

      # TextBlob version
      for w in tokens:
        checked = Word(w).spellcheck()
        if not checked[0][0] == w:
          if not w in words:
            words[w] = 0
          words[w] += 1
    except:
      print("ERROR")

  if len(words) > 100:
    sort = sorted(words.items(), key=operator.itemgetter(1))[-100:]
  else:
    sort = sorted(words.items(), key=operator.itemgetter(1))

  with open(folder_path + str(year) + ".p", 'wb') as file:
    pickle.dump(sort, file, protocol=0)
