# coding: utf-8
import config as CONFIG
import pickle

with open(CONFIG.datasets_path + "detalles_subtitulos.p", 'rb') as f:
    subtitles_index = pickle.load(f)

filtered_index = subtitles_index[["english" in e.lower() for e in [str(e) for e in subtitles_index.imdb_language]]]
filtered_index = filtered_index[[("usa" in e.lower()) or (("uk" in e.lower())) or (("canada" in e.lower())) or (("australia" in e.lower())) for e in [str(e) for e in filtered_index.imdb_country]]]
filtered_index = filtered_index[filtered_index.imdb_kind == "movie"]
filtered_index.to_pickle(CONFIG.datasets_path + "filtered_index.p")
filtered_index.to_csv(CONFIG.datasets_path + "filtered_index.txt", sep="\t", index=False)

print("Total nº of subs: ", len(filtered_index.index))
