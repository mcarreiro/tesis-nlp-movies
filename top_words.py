import pandas as pd
import config as CONFIG
import pickle

with open(CONFIG.datasets_path + "frequency_index.p", 'rb') as f:
  index = pickle.load(f)

df = pd.DataFrame.from_dict(index, orient='index')

top_words = {}
years = [str(year) for year in range(1930,2014)]
for year in years:
  top_words[year] = df.sort_values(year, ascending=False)[year][1:100].index.tolist()


with open(CONFIG.datasets_path + "top_words.p", 'wb') as file:
  pickle.dump(top_words, file, protocol=pickle.HIGHEST_PROTOCOL)

