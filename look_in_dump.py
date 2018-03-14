# -*- coding: utf-8 -*-
import pandas as pd
import gzip
import config as CONFIG
import re
import os


def file_name(movie_file_number, subtitles_path=CONFIG.subtitles_path):
    """ Arma el nombre de archivo para abrir el srt """
    tmp_name = zip(movie_file_number, movie_file_number[::-1])
    file_path = [subtitles_path.replace("_popular", "")]
    file_name = []

    for i, (s1, s2) in enumerate(tmp_name):
        file_name.append(s1)
        if i < 4:
            file_path.insert(0, s2 + "/")

    return "".join(file_path[::-1]) + "".join(file_name) + ".gz"


top_movies = pd.read_csv(CONFIG.datasets_path + "filtered_index.txt", sep="\t")
export_data = pd.read_csv(CONFIG.subtitles_path.replace("_popular", "") + "export.txt", sep="\t")
subs_file_location = dict(zip(export_data.IDSubtitle, export_data.IDSubtitleFile))

# Pego la columna de urls
urls = []
for i, m in enumerate(top_movies.MovieImdbID):
    if not i % 100:
        print(i)
    with open(CONFIG.datasets_path + "urls/" + str(m) + ".txt", "rb") as f:
        urls.append(f.read().decode("utf-8"))
top_movies["urls"] = urls

# Extraigo los ids de subtitulos y pego como columna
sub_ids = []
for s in [re.compile("\/(\d+)$").findall(e) for e in top_movies.urls]:
    if s:
        sub_ids.append(s[0])
    else:
        sub_ids.append(None)
top_movies["sub_id"] = sub_ids

# Found srt
found_srt = set(os.listdir(CONFIG.subtitles_path))

# Guardo los subtitulos en una carpeta
sub_srt_files = []
for i, s in enumerate(sub_ids):
    if not i % 100:
        print(i)
    if not s:
        sub_srt_files.append(s)
    else:
        if str(s) + ".srt" in found_srt:  # Si ya lo había encontrado
            sub_srt_files.append("available")
        elif int(s) in subs_file_location:
            file_location = file_name(str(subs_file_location[int(s)]))
            try:
                with gzip.open(file_location) as f:
                    file_content = f.read()
                file_dest = CONFIG.datasets_path + "subtitulos_popular/" + s + ".srt"
                with open(file_dest, "wb") as f:
                    f.write(file_content)
                sub_srt_files.append("available")
            except Exception:
                sub_srt_files.append("to_search")
        else:
            sub_srt_files.append("to_search")

top_movies["srt_to_search"] = sub_srt_files

top_movies.to_csv(CONFIG.datasets_path + "filtered_index.txt", sep="\t", index=False)
