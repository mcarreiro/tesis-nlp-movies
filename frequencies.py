from Subtitle import Subtitle
import pandas as pd
import config as CONFIG
import pickle
import matplotlib.pyplot as plt

class Analyzer(object):

  def __init__(self):
    with open(CONFIG.datasets_path + "manual_inverted_index.p", 'rb') as f:
      self.index = pickle.load(f)

    with open(CONFIG.datasets_path + "filtered_index.p", 'rb') as f:
      self.sub_data = pickle.load(f)

    with open(CONFIG.datasets_path + "word_count.p", 'rb') as f:
      self.count_per_year = pickle.load(f)

  def word_frequency_for(self, word):
    if word not in self.index:
      print("This word is not in the index")
      return None;
    else:
      mentions = self.index[word] # With repeated occurrences
      filtered = self.sub_data[["MovieYear","IDSubtitleFile"]][self.sub_data.IDSubtitleFile.isin(mentions)]
      # Non working attempt:
      # sub_data["Normalizado"] = sub_data[["MovieYear","MovieID"]].groupby("MovieYear").agg({'MovieID': 'count'}).apply(lambda row: normalize_count(row.name,row["MovieYear"]))
      dic = filtered.groupby("MovieYear").count().to_dict()["IDSubtitleFile"]

      condensed = {}
      for i, row in filtered.iterrows():
        if not row.MovieYear in condensed:
          condensed[row.MovieYear] = 0
        condensed[row.MovieYear] += mentions.count(row.IDSubtitleFile)

      result = {}
      for key, value in dic.items():
        # Mentions / word total
        if key in self.count_per_year:
          result[key] = condensed[key] / self.count_per_year[key]
        # Movies / movie total (using movie_count.p in line 16)
        # result[key] = value / self.count_per_year[key]

      sorted_tuples = [(k, result[k]) for k in sorted(result)]
      sorted_tuples = [(k, Analyzer.res_or_zero(result, k)) for k in range(int(sorted_tuples[0][0]), int(sorted_tuples[len(sorted_tuples)-1][0]))]
      plt.bar(range(len(sorted_tuples)), [v for k,v in sorted_tuples])
      plt.xticks(range(len(sorted_tuples)), [k for k,v in sorted_tuples])
      locs, labels = plt.xticks()
      plt.setp(labels, rotation=90)
      plt.title("Word frequency for '%(word)s'" % locals())
      plt.show()
      return sorted_tuples

  @staticmethod
  def res_or_zero(res, k):
    if k in res:
      return res[k]
    else:
      return 0
