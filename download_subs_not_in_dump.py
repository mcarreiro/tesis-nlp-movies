# coding: utf-8
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import re
import pandas as pd
from time import sleep
import os
from random import random
import config as CONFIG
import zipfile

subs_folder = CONFIG.datasets_path + "subs_not_in_dump/"

top_movies = pd.read_csv(CONFIG.datasets_path + "filtered_index.txt", sep="\t")
mask = top_movies.srt_to_search == "to_search"
mask = mask & (top_movies.imdb_year < 2017)
to_search = top_movies[mask]["urls"]


def reiniciaThor():
    os.system('killall tor')
    sleep(0.3)
    os.system('tor &')
    while os.system('ps | grep tor') != 0:
        pass
    return


def open_driver(subs_folder=subs_folder, tor_enabled=False):
    os.system("killall firefox")
    profile = FirefoxProfile()
    # Para bajar los zip
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", subs_folder)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/zip')
    # Para entrar con tor
    if tor_enabled:
        reiniciaThor()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.dns.disablePrefetch', True)
        profile.set_preference('network.proxy.socks_remote_dns', True)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9050)

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get("https://www.opensubtitles.org")
    return driver


driver = open_driver(subs_folder, tor_enabled=False)

downloaded = set([re.compile("\d+").findall(e)[-1] for e in os.listdir(subs_folder) if e.endswith(".zip")])
for i, m in enumerate(to_search):
    if m.split("/")[-1] in downloaded:
        continue
    print(m)
    url = "https://www.opensubtitles.org" + m
    driver.get(url)
    sleep(1 + (1 - 0) * random())
    elem = driver.find_elements_by_link_text("Download")[0]
    elem.click()


downloaded = [e for e in os.listdir(subs_folder) if e.endswith(".zip")]

for s in downloaded:
    print(s)
    zp = zipfile.ZipFile(subs_folder + s)
    filenames = zp.namelist()
    if 'The Panic in Needle Park 1971.txt' in filenames:
        filename = 'The Panic in Needle Park 1971.txt'
    elif 'Money.2016.720p.BluRay.x264-.YTS.AG.SRT' in filenames:
        filename = 'Money.2016.720p.BluRay.x264-.YTS.AG.SRT'
    elif 'Last of the Comanches (1953) Eng.txt' in filenames:
        filename = 'Last of the Comanches (1953) Eng.txt'
    elif 'The Proud Rebel (1958) Eng.txt' in filenames:
        filename = 'The Proud Rebel (1958) Eng.txt'
    elif 'Gun Shy.txt' in filenames:
        filename = 'Gun Shy.txt'
    elif 'Seminole (1953) Eng.txt' in filenames:
        filename = 'Seminole (1953) Eng.txt'
    elif 'Rolf de Heer - Dingo - EngtoEng.txt' in filenames:
        filename = 'Rolf de Heer - Dingo - EngtoEng.txt'
    elif 'Crossplot 1969.txt' in filenames:
        filename = 'Crossplot 1969.txt'
    elif 'Rhymes.for.Young.Ghouls.2013.720p.BRRip.x264-YIFY.en.txt' in filenames:
        filename = 'Rhymes.for.Young.Ghouls.2013.720p.BRRip.x264-YIFY.en.txt'
    else:
        filename = [e for e in filenames if "srt" in e][0]
    with open(CONFIG.datasets_path + "subtitulos_popular/" + re.compile("\d+").findall(s)[-1] + ".srt", "wb") as f:
        f.write(zp.read(filename))

subs_data = set(os.listdir(CONFIG.datasets_path + "subtitulos_popular/"))
for s in top_movies.loc[top_movies.imdb_year < 2017].sub_id:
    if pd.isna(s):
        continue
    if not str(int(s)) + ".srt" in subs_data:
        raise Exception
