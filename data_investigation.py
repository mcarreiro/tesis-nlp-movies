import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl
import pickle

datasets_path = "/Users/vale/Facultad/Tesis/data/datasets/"

with open(datasets_path + "detalles_subtitulos.p", 'rb') as f:
  subtitles_index = pickle.load(f, encoding='latin-1')

print("Cantidad de películas diferentes: ", len(pd.value_counts(subtitles_index['MovieID'])))

gr = subtitles_index[['MovieID','MovieYear']].groupby('MovieYear')
chart = gr.count().plot(kind='bar')
chart.xaxis.set_ticklabels(chart.xaxis.get_ticklabels(), rotation=45)
for i, label in enumerate(chart.xaxis.get_ticklabels()):
  if not i % 4 == 0:
    label.set_visible(False)
mpl.savefig('investigation_charts/movies_by_year.png', bbox_inches='tight')


gr = subtitles_index[subtitles_index.MovieYear >= 1950][['MovieID','MovieYear']].groupby('MovieYear')
chart = gr.count().plot(kind='bar')
for label in chart.xaxis.get_ticklabels()[::2]:
  label.set_visible(False)
mpl.savefig('investigation_charts/movies_by_year_over_50s.png', bbox_inches='tight')


gr = subtitles_index[['MovieID','SubLanguageID']].groupby('SubLanguageID')
chart = gr.count().plot(kind='bar')
mpl.savefig('investigation_charts/movies_by_sublang.png', bbox_inches='tight')


gr = subtitles_index[['MovieID','SubFormat']].groupby('SubFormat')
chart = gr.count().plot(kind='bar')
mpl.savefig('investigation_charts/movies_by_format.png', bbox_inches='tight')


No es pertinente, es todos los lenguajes en los que hay diálogo en la película
gr = subtitles_index[['MovieID','Language']].groupby('Language')
chart = gr.count().plot(kind='bar')
mpl.savefig('investigation_charts/movies_by_lang.png', bbox_inches='tight')


gr = subtitles_index[["MovieID","Country"]][subtitles_index.Country.str.contains("USA", na=False)].groupby('Country').filter(lambda x: len(x) > 50).groupby("Country")
chart = gr.count().plot(kind='bar')
mpl.savefig('investigation_charts/movies_from_usa.png', bbox_inches='tight')


gr = subtitles_index[['MovieID','Type']].groupby('Type')
chart = gr.count().plot(kind='bar')
mpl.savefig('investigation_charts/movies_by_type.png', bbox_inches='tight')


gr = subtitles_index[['MovieID','imdbRating']].groupby('imdbRating')
chart = gr.count().plot(kind='bar')
for label in chart.xaxis.get_ticklabels()[::2]:
  label.set_visible(False)
mpl.savefig('investigation_charts/movies_by_rating.png', bbox_inches='tight')
