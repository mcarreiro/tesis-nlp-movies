from Subtitle import Subtitle
from pathos.multiprocessing import ProcessingPool as Pool
import os
import config as CONFIG
import pickle
import pandas as pd

top_movies = pd.read_csv(CONFIG.datasets_path + "filtered_index.txt", sep="\t")
top_movies = top_movies[(top_movies.sub_id.notnull()) & (top_movies.imdb_year < 2017)]


def check_symmetry(contexts, sub_id):
    for i, t1 in enumerate(contexts):
        for t2 in contexts[t1]:
            if (t1 not in contexts[t2]) or (t2 not in contexts[t1]) or (not (contexts[t1][t2] == contexts[t2][t1])):
                print(sub_id)
                return False
    return True


def gen_contexts(sub_id, length):

    path = CONFIG.datasets_path + ("contexts/%02d/" % length)
    if str(sub_id) + "_contexts.p" in DONE:
        return None
    sub = Subtitle(sub_id)
    tokens = sub.full_tokens()
    contexts = sub.generate_word_contexts(length)
    len_windows = sub.len_windows
    if not check_symmetry(contexts, sub_id):
        aaa

    with open(path + str(sub_id) + "_tokens.p", "wb") as f:
        pickle.dump(tokens, f)

    with open(path + str(sub_id) + "_contexts.p", "wb") as f:
        pickle.dump(contexts, f)

    with open(path + str(sub_id) + "_len_windows.p", "wb") as f:
        pickle.dump(len_windows, f)


sub_ids = [int(e.sub_id) for e in top_movies.itertuples()]

#gen_contexts(sub_ids[0], 45)

"""
DONE = set(os.listdir(CONFIG.datasets_path + ("contexts/%02d/" % 45)))
for i, s in enumerate(sub_ids):
    gen_contexts(s, 45)
    #print(i, "bbb")
"""

for l in [30, 15, 45]:
    DONE = set(os.listdir(CONFIG.datasets_path + ("contexts/%02d/" % l)))
    with Pool(8) as p:
        p.map(gen_contexts, sub_ids, [l] * len(sub_ids))
