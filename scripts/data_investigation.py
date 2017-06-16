import sys
sys.path.append('..')
from repo import config as CONFIG
import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl
import pickle

mpl.style.use('ggplot')
from pylab import rcParams
rcParams['figure.figsize'] = 10, 6
# print(rcParams)

with open(CONFIG.datasets_path + "detalles_subtitulos.p", 'rb') as f:
  subtitles_index = pickle.load(f, encoding='latin-1')

subtitles_index = subtitles_index.drop_duplicates(subset='MovieID')

# print("Cantidad de películas diferentes: ", len(pd.value_counts(subtitles_index['MovieID'])))

# gr = subtitles_index[['MovieID','MovieYear']].groupby('MovieYear')
# chart = gr.count().plot(kind='bar')
# chart.legend(labels=['Originales distintos'])
# for i, label in enumerate(chart.xaxis.get_ticklabels()):
#   if not i % 2 == 0:
#     label.set_visible(False)
# mpl.savefig('investigation_charts/full_by_year.png', bbox_inches='tight')

# gr = subtitles_index[['MovieID','Type']].groupby('Type')
# chart = gr.count().plot(kind='bar')
# chart.legend(labels=['Originales distintos'])
# rects = chart.patches
# labels = gr.count()["MovieID"].tolist()
# for rect, label in zip(rects, labels):
#   height = rect.get_height()
#   chart.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom', color=rcParams['axes.labelcolor'])
# mpl.savefig('investigation_charts/full_by_type.png', bbox_inches='tight')

movies = subtitles_index[subtitles_index.Type.isin(['movie'])]
# gr = subtitles_index[subtitles_index.MovieYear >= 1950][['MovieID','MovieYear']].groupby('MovieYear')
# chart = gr.count().plot(kind='bar')
# for label in chart.xaxis.get_ticklabels()[::2]:
#   label.set_visible(False)
# mpl.savefig('investigation_charts/movies_by_year_over_50s.png', bbox_inches='tight')


# gr = subtitles_index[subtitles_index.Type == 'movie'][subtitles_index.MovieYear >= 1950][['MovieID','MovieYear']].groupby('MovieYear')
# chart = gr.count().plot(kind='bar')
# for label in chart.xaxis.get_ticklabels()[::2]:
#   label.set_visible(False)
# mpl.savefig('investigation_charts/filtered_movies_by_year.png', bbox_inches='tight')


# gr = movies[['MovieID','SubLanguageID']].groupby('SubLanguageID')
# chart = gr.count().plot(kind='bar')
# chart.legend(labels=['Películas distintas'])
# mpl.savefig('investigation_charts/movies_by_sublang.png', bbox_inches='tight')


# gr = movies[['MovieID','SubFormat']].groupby('SubFormat')
# chart = gr.count().plot(kind='bar')
# mpl.savefig('investigation_charts/movies_by_format.png', bbox_inches='tight')


# No es pertinente, es todos los lenguajes en los que hay diálogo en la película
# gr = subtitles_index[['MovieID','Language']].groupby('Language')
# chart = gr.count().plot(kind='bar')
# mpl.savefig('investigation_charts/movies_by_lang.png', bbox_inches='tight')


# gr = subtitles_index[["MovieID","Country"]][subtitles_index.Country.str.contains("USA", na=False)].groupby('Country').filter(lambda x: len(x) > 50).groupby("Country")
# chart = gr.count().plot(kind='bar')
# mpl.savefig('investigation_charts/movies_from_usa.png', bbox_inches='tight')


# Este lo hice por diversión
# gr = subtitles_index[['MovieID','imdbRating']].groupby('imdbRating')
# chart = gr.count().plot(kind='bar')
# for label in chart.xaxis.get_ticklabels()[::2]:
#   label.set_visible(False)
# mpl.savefig('investigation_charts/movies_by_rating.png', bbox_inches='tight')

movies = movies[subtitles_index.Country.str.contains("USA", na=False)][movies.Country.str.contains("USA", na=False)]
gr = movies[['MovieID','MovieYear']].groupby('MovieYear')
chart = gr.count().plot(kind='bar')
chart.legend(labels=['Películas distintas'], loc=2)
for i, label in enumerate(chart.xaxis.get_ticklabels()):
  if not i % 2 == 0:
    label.set_visible(False)
mpl.savefig('investigation_charts/filtered_by_year.png', bbox_inches='tight')
