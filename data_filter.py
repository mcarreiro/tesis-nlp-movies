import pandas as pd
import matplotlib.pyplot as mpl
import pickle
import filtrado

datasets_path = "/Users/vale/Facultad/Tesis/data/datasets/"

with open(datasets_path + "detalles_subtitulos.p", 'rb') as f:
  subtitles_index = pickle.load(f, encoding='latin-1')


filtered_index = subtitles_index[subtitles_index.Country == "USA"]
filtered_index = filtered_index[filtered_index.Language.str.contains("English", na=False)]
filtered_index = filtered_index[filtered_index.SubSumCD == 1]
filtered_index = filtered_index[filtered_index.Type == 'movie']
filtered_index = filtrado.best_subs(filtered_index)

filtered_index.to_pickle(datasets_path + "filtered_index.p")
