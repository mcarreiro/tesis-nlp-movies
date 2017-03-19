import sys
sys.path.append('..')
from repo import config as CONFIG
import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl
import pickle

with open(CONFIG.datasets_path + "filtered_index.p", 'rb') as f:
  subtitles_index = pickle.load(f, encoding='latin-1')

print("Total nº of subs: ", len(subtitles_index.index))

# Gráfico del dataset final
gr = subtitles_index[['MovieID','MovieYear']].groupby('MovieYear')
chart = gr.count().plot(kind='bar')
chart.xaxis.set_ticklabels(chart.xaxis.get_ticklabels(), rotation=45)
for i, label in enumerate(chart.xaxis.get_ticklabels()):
  if not i % 4 == 0:
    label.set_visible(False)
mpl.savefig('investigation_charts/filtered.png', bbox_inches='tight')


# 50's on
gr = subtitles_index[subtitles_index.MovieYear >= 1950][['MovieID','MovieYear']].groupby('MovieYear')
chart = gr.count().plot(kind='bar')
for label in chart.xaxis.get_ticklabels()[::2]:
  label.set_visible(False)
mpl.savefig('investigation_charts/filtered_after_50.png', bbox_inches='tight')
