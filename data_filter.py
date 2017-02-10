import pandas as pd
import matplotlib.pyplot as mpl
import pickle
import filtrado
import config as CONFIG

with open(CONFIG.datasets_path + "detalles_subtitulos.p", 'rb') as f:
  subtitles_index = pickle.load(f, encoding='latin-1')


# filtered_index = subtitles_index[subtitles_index.Country == "USA"]
filtered_index = subtitles_index[subtitles_index.Country.str.contains("USA", na=False)]
filtered_index = filtered_index[filtered_index.Language.str.contains("English", na=False)]
filtered_index = filtered_index[filtered_index.SubSumCD == 1]
filtered_index = filtered_index[filtered_index.Type.isin(['movie'])]
filtered_index = filtrado.best_subs(filtered_index)

filtered_index.to_pickle(CONFIG.datasets_path + "filtered_index_2017.p")
# filtered_index.to_pickle(CONFIG.datasets_path + "filtered_index_with_series.p")

print("Total nº of subs: ", len(filtered_index.index))
