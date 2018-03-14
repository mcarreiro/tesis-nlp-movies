# coding: utf-8
import urllib.request
import os
import re
import pickle
import config as CONFIG
from bs4 import BeautifulSoup
from random import shuffle

with open(CONFIG.datasets_path + "filtered_index.p", "rb") as f:
    movie_data = pickle.load(f)

urls_folder = CONFIG.datasets_path + "urls/"


def download_url(MovieImdbID):
    base_url = "https://www.opensubtitles.org/en/search/sublanguageid-eng/subsumcd-1/subformat-srt/imdbid-%d/sort-7/asc-0"
    raw = urllib.request.urlopen(base_url % MovieImdbID).read().decode("utf-8")
    soup = BeautifulSoup(raw)

    if not soup.findAll(class_="logo"):
        return "not_loaded"

    if "numberofEpisodes" in raw:
        return "series"

    try:
        return re.compile("/en/subtitleserve/sub/\d+").findall(raw)[0]
    except Exception:
        return "no_subtitle"


movies = list(set(movie_data.MovieImdbID))

shuffle(movies)

downloaded = set(os.listdir(urls_folder))

not_found = 0
for i, m in enumerate(movies):
    if str(m) + ".txt" in downloaded:
        continue
    not_found += 1
    print(i, m)
    url = download_url(m)
    if url == "not_loaded":
        continue
    elif url == "series":
        content = "series"
    else:
        content = url
    print(content)
    with open(urls_folder + str(m) + ".txt", "wb") as f:
        f.write(content.encode("utf-8"))
