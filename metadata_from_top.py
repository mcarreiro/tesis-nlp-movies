# -*- coding: utf-8 -*-
import pandas as pd
import urllib3
import pickle
import time
from random import random
import os
import sys
sys.path.append('..')
import config as CONFIG

http = urllib3.PoolManager()

metadata_folder = CONFIG.datasets_path + "metadata/"

top_movies = pd.read_csv(CONFIG.datasets_path + "top_movies_by_year.txt", sep="\t", quotechar='"', encoding='utf-8')
peliculas = set(top_movies.MovieImdbID)

# Campos que se van a considerar
campos = ['kind', 'year', 'language', 'genre', 'country', 'rating', 'title']

# A los datos guardados lo agrego a un diccionario
metadata = {}
encontrados = os.listdir(metadata_folder)

for i, p in enumerate(filter(lambda x: x.endswith(".p"), encontrados)):
    if p == "1637574.p":  # Porque Conan no se puede bajar de la API
        continue
    if i % 100 == 0:
        print(i)
    with open(metadata_folder + p, "rb") as f:
        md = pickle.load(f)
        m = dict([(e, md.get(e, pd.np.nan)) for e in campos])
    metadata[p.split(".")[0]] = m

with open(CONFIG.datasets_path + "metadata.p", "wb") as f:
    pickle.dump(metadata, f)

indices = metadata.keys()

matriz_metadata_tmp = []
for i, p in enumerate(indices):  # Hago una limpieza de la metadata, viene como texto
    row = []
    for c in campos:
        row.append(metadata[p][c])
    row.append(p)
    matriz_metadata_tmp.append(row)

# Conan is not found by the api
matriz_metadata_tmp.append(['tv series', 2010.0, ['English'],
                            ['Comedy', 'Music', 'Talk-Show'],
                            ['USA'], 8.1, 'Conan', 1637574])

matriz_metadata = pd.DataFrame(matriz_metadata_tmp,
                               columns=["imdb_" + e for e in campos] + ["MovieImdbID"])

matriz_metadata.to_csv("metadata.txt", sep="\t", index=False)

# Cast the same type for a good merge
matriz_metadata.MovieImdbID = matriz_metadata.MovieImdbID.astype(int)
top_movies.MovieImdbID = top_movies.MovieImdbID.astype(int)

top_movies = top_movies.merge(matriz_metadata, how='left', on='MovieImdbID')
top_movies.to_pickle(CONFIG.datasets_path + "detalles_subtitulos.p")
top_movies.to_csv("detalles_subtitulos.txt", sep="\t", index=False)
