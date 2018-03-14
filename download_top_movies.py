# coding: utf-8
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import config as CONFIG

url = "http://www.imdb.com/search/title?release_date=%d&sort=boxoffice_gross_us,desc&page=%d"

dataset = []
years = range(1930, 2018)

for y in years:
    page = 0
    year_rank = 0
    keep_on_year = True
    while keep_on_year:
        print(y, page + 1)
        raw = urllib.request.urlopen(url % (y, page + 1)).read().decode("utf-8")
        soup = BeautifulSoup(raw, "lxml")
        list_items = soup.find_all(attrs={'class': 'lister-item-header'})
        for li in list_items:
            dataset.append([y,
                            year_rank + 1,
                            li.a.text,
                            li.a["href"].split("/")[2],
                            int(li.a["href"].split("/")[2].replace("tt", ""))])
            year_rank += 1
            if year_rank == 1000:
                keep_on_year = False
                break
        page += 1

header = ["year", "rank", "title", "orig_MovieImdbID", "MovieImdbID"]

pd.DataFrame(dataset, columns=header).to_csv(CONFIG.datasets_path + "top_movies_by_year.txt",
                                             sep="\t", index=False,
                                             encoding="utf-8")
