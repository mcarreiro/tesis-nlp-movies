import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl
import pickle

datasets_path = "/Users/vale/Facultad/Tesis/data/datasets/"

with open(datasets_path + "filtered_index.p", 'rb') as f:
  subtitles_index = pickle.load(f, encoding='latin-1')

# Gráfico del dataset final
gr = subtitles_index[['MovieID','MovieYear']].groupby('MovieYear')
chart = gr.count().plot(kind='bar')
chart.xaxis.set_ticklabels(chart.xaxis.get_ticklabels(), rotation=45)
for i, label in enumerate(chart.xaxis.get_ticklabels()):
  if not i % 4 == 0:
    label.set_visible(False)
mpl.savefig('investigation_charts/filtered.png', bbox_inches='tight')
