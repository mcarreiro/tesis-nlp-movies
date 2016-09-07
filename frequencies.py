from Subtitle import Subtitle
import pandas as pd
import config as CONFIG
import pickle

class Analyzer(object):

  def __init__(self):
    with open(CONFIG.datasets_path + "manual_inverted_index.p", 'rb') as f:
      self.index = pickle.load(f)

    with open(CONFIG.datasets_path + "filtered_index.p", 'rb') as f:
      self.sub_data = pickle.load(f)

  def word_frequency_for(self, word):
    if word not in self.index:
      print("This word is not in the index")
      return None;
    else:
      mentions = set(self.index[word])
      # This is not a reasonable measurement. Normalisation has to be done somehow.
      return self.sub_data[["MovieYear","IDSubtitleFile"]][self.sub_data.IDSubtitleFile.isin(list(mentions))].groupby("MovieYear").count()
